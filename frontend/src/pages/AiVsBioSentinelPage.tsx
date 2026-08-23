import React from 'react';
import { AiVsBioSentinel } from '../components/AiVsBioSentinel';
import { SafetyDisclaimerBanner } from '../components/SafetyDisclaimerBanner';

export const AiVsBioSentinelPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <SafetyDisclaimerBanner />
      <AiVsBioSentinel />
    </div>
  );
};
