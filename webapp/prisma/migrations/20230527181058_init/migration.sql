-- CreateEnum
CREATE TYPE "JobState" AS ENUM ('PENDING', 'RUNNING', 'ERROR', 'COMPLETE');

-- CreateTable
CREATE TABLE "PredictionJob" (
    "id" INT8 NOT NULL DEFAULT unique_rowid(),
    "question" STRING NOT NULL,
    "state" "JobState" NOT NULL,
    "public" BOOL NOT NULL DEFAULT true,
    "errorMessage" STRING,
    "modelTemperature" INT4 NOT NULL,
    "resultProbability" INT4 NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "userId" STRING NOT NULL,

    CONSTRAINT "PredictionJob_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PredictionJobLog" (
    "id" INT8 NOT NULL DEFAULT unique_rowid(),
    "logText" STRING NOT NULL,
    "jobId" INT8 NOT NULL,

    CONSTRAINT "PredictionJobLog_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "User" (
    "id" STRING NOT NULL,
    "email" STRING,
    "credits" INT4 NOT NULL DEFAULT 0,
    "creditsPurchased" INT4 NOT NULL DEFAULT 0,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "PredictionJob_state_createdAt_idx" ON "PredictionJob"("state", "createdAt" DESC);

-- CreateIndex
CREATE UNIQUE INDEX "User_id_key" ON "User"("id");

-- AddForeignKey
ALTER TABLE "PredictionJob" ADD CONSTRAINT "PredictionJob_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PredictionJobLog" ADD CONSTRAINT "PredictionJobLog_jobId_fkey" FOREIGN KEY ("jobId") REFERENCES "PredictionJob"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
