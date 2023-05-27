const { PrismaClient } = require('@prisma/client');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const prisma = new PrismaClient();

const APP_ID = 'oracle';

exports.handler = async (event, context) => {
  const sig = event.headers['stripe-signature'];

  let stripeEvent;
  try {
    stripeEvent = stripe.webhooks.constructEvent(
      event.body,
      sig,
      process.env.STRIPE_PAYMENT_ENDPOINT_SECRET
    );
  } catch (err) {
    return {
      statusCode: 400,
      body: JSON.stringify({ success: false, error: err.message }),
    };
  }
  switch (stripeEvent.type) {
    case 'checkout.session.completed':
      const checkoutSessionCompleted = stripeEvent.data.object;
      const refId = checkoutSessionCompleted.client_reference_id;
      const [appId, userId] = refId.split(':::');
      if (appId !== APP_ID) {
        console.warn('AppId mismatch', appId);
      } else if (userId) {
        const user = await prisma.User.findFirst({
          where: { userId: userId },
        });
        await prisma.User.update({
          where: { id: userId },
          data: {
            credits: user.credits + 100,
            email: checkoutSessionCompleted.customer_details.email,
          },
        });
      } else {
        console.error('No userId found for checkout session');
      }
      break;
    default:
      console.log(`Unhandled event type ${stripeEvent.type}`);
  }
  return {
    statusCode: 200,
    body: JSON.stringify({ success: true }),
  };
};
