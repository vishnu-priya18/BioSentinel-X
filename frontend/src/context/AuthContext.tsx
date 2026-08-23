import React, { createContext, useContext, useState } from 'react';
import { UserRole } from '../types';

interface AuthContextType {
  userRole: UserRole;
  userName: string;
  setUserRole: (role: UserRole) => void;
  setUserName: (name: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [userRole, setUserRole] = useState<UserRole>('SUPERVISOR');
  const [userName, setUserName] = useState<string>('Anita Roy (Supervisor)');

  const logout = () => {
    setUserRole('VIEWER');
    setUserName('Guest Viewer');
  };

  return (
    <AuthContext.Provider value={{ userRole, userName, setUserRole, setUserName, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
