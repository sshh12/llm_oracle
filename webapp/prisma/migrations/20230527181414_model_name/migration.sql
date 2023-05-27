/*
  Warnings:

  - Added the required column `modelName` to the `PredictionJob` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "PredictionJob" ADD COLUMN     "modelName" STRING NOT NULL;
