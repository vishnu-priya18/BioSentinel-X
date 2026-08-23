import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';

// Pages
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { ScanWastePage } from './pages/ScanWastePage';
import { VerificationQueuePage } from './pages/VerificationQueuePage';
import { WastePassportPage } from './pages/WastePassportPage';
import { EvidenceExplorerPage } from './pages/EvidenceExplorerPage';
import { CollectionTasksPage } from './pages/CollectionTasksPage';
import { DigitalTwinPage } from './pages/DigitalTwinPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { AiSafetyEvaluationPage } from './pages/AiSafetyEvaluationPage';
import { AuditTrailPage } from './pages/AuditTrailPage';
import { SimulationModePage } from './pages/SimulationModePage';
import { AiVsBioSentinelPage } from './pages/AiVsBioSentinelPage';
import { AlertsPage } from './pages/AlertsPage';
import { UserManagementPage } from './pages/UserManagementPage';
import { DepartmentManagementPage } from './pages/DepartmentManagementPage';
import { WasteCategoryManagementPage } from './pages/WasteCategoryManagementPage';
import { RegulatoryConfigPage } from './pages/RegulatoryConfigPage';
import { SettingsPage } from './pages/SettingsPage';
import { ProfilePage } from './pages/ProfilePage';

const AppLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 antialiased selection:bg-cyan-500 selection:text-black">
      <Navbar />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar />
        <main className="flex-1 p-6 overflow-y-auto max-w-[1800px] w-full mx-auto">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/scan" element={<ScanWastePage />} />
            <Route path="/verification" element={<VerificationQueuePage />} />
            <Route path="/collection" element={<CollectionTasksPage />} />
            <Route path="/passports" element={<WastePassportPage />} />
            <Route path="/evidence" element={<EvidenceExplorerPage />} />
            <Route path="/ai-vs-biosentinel" element={<AiVsBioSentinelPage />} />
            <Route path="/intelligence" element={<DigitalTwinPage />} />
            <Route path="/digital-twin" element={<DigitalTwinPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/ai-safety" element={<AiSafetyEvaluationPage />} />
            <Route path="/alerts" element={<AlertsPage />} />
            <Route path="/audit" element={<AuditTrailPage />} />
            <Route path="/simulation" element={<SimulationModePage />} />
            <Route path="/users" element={<UserManagementPage />} />
            <Route path="/departments" element={<DepartmentManagementPage />} />
            <Route path="/categories" element={<WasteCategoryManagementPage />} />
            <Route path="/regulatory" element={<RegulatoryConfigPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/*" element={<AppLayout />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
