const { PrismaClient, JobState } = require('@prisma/client');

const prisma = new PrismaClient();

exports.handler = async (event, context) => {
  const { model, temp, public, userId, q } = event.queryStringParameters;
  if (!userId) {
    return {
      statusCode: 400,
      body: '{}',
    };
  }
  const modelTemperature = parseInt(temp);
  let job = await prisma.PredictionJob.findFirst({
    where: {
      question: q,
      state: { in: [JobState.COMPLETE, JobState.PENDING] },
      modelTemperature: modelTemperature,
    },
  });
  if (!job) {
    job = await prisma.PredictionJob.create({
      data: {
        userId: userId,
        modelName: model,
        question: q,
        modelTemperature: modelTemperature,
        public: public === 'true',
        resultProbability: 50,
        state: JobState.PENDING,
      },
    });
  }
  return {
    statusCode: 302,
    headers: {
      Location: `/results/${job.id}`,
    },
  };
};
