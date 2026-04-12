// app/dashboard/page.js
import { Suspense } from 'react';
import DashboardContent from './DashboardContent';

export default function DashboardPage() {
  return (
    <Suspense fallback={<div>로딩 중...</div>}>
      <DashboardContent />
    </Suspense>
  );
}