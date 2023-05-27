const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

exports.handler = async (event, context) => {
  const { jobId } = event.queryStringParameters;
  if (!jobId) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'jobId' }),
    };
  }
  const job = await prisma.PredictionJob.findFirst({
    where: { id: BigInt(jobId) },
    include: { logs: true },
  });
  console.log(job.logs);
  const logs = job.logs
    .sort((a, b) => a.createdAt - b.createdAt)
    .map(l => l.logText);
  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        id: job.id,
        state: job.state,
        question: job.question,
        errorMessage: job.errorMessage,
        resultProbability: job.resultProbability,
        logs: logs,
      },
      (_key, value) => (typeof value === 'bigint' ? value.toString() : value)
    ),
  };
};
