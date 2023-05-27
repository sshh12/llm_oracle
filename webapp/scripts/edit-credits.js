const { PrismaClient } = require('@prisma/client');
const readline = require('readline');

const prisma = new PrismaClient();

function prompt(query) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise(resolve =>
    rl.question(query, ans => {
      rl.close();
      resolve(ans);
    })
  );
}

(async () => {
  const userId = await prompt('UserId: ');
  let user = await prisma.User.findFirst({
    where: { id: userId },
  });
  if (!user) {
    const email = await prompt('email: ');
    user = await prisma.User.create({ data: { email: email, id: userId } });
  }
  console.log(user);
  const credits = parseInt(await prompt('credits: '));
  if (credits) {
    await prisma.User.update({
      where: { id: userId },
      data: {
        credits: credits,
      },
    });
  }
})();
