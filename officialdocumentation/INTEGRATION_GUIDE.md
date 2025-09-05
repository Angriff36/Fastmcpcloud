# 🔗 Package Integration Guide

## Integration Workflow

### 1. **Independent Development Phase**
```bash
# Develop each package independently
cd packages/ui-components && npm run design-system    # Design UI
cd packages/auth && npm run demo                      # Build auth flows
cd packages/features-ocr && npm run demo              # Build OCR features
cd packages/features-prep-lists && npm run demo       # Build task management
cd packages/features-settings && npm run demo         # Build settings
```

### 2. **Build Phase**
```bash
# Build all packages for integration
npm run build:packages
```

### 3. **Integration Phase**
```bash
# Start the full app with all packages integrated
npm run dev
```

## How Packages Get Combined

### **Import Pattern in Main App**
```tsx
// src/App.tsx - Main application file
import { useCompanyAuth, CompanyLogin } from '@prep-chef/auth';
import { Button, Card, LoadingSpinner } from '@prep-chef/ui-components';
import { usePrepLists } from '@prep-chef/features-prep-lists';
import { useSettings } from '@prep-chef/features-settings';
import { useOCR } from '@prep-chef/features-ocr';

function App() {
  // 🔐 Authentication state from auth package
  const { user, company, login, logout } = useCompanyAuth();
  
  // 📋 Prep lists functionality from prep-lists package
  const { prepLists, createList, updateList } = usePrepLists();
  
  // ⚙️ Settings from settings package
  const { settings, updateSettings } = useSettings();
  
  // 📱 OCR functionality from OCR package
  const { scanDocument, extractText } = useOCR();

  return (
    <div>
      {/* 🔐 Use auth components */}
      {!user ? (
        <CompanyLogin onLogin={login} />
      ) : (
        <div>
          {/* 🎨 Use UI components */}
          <Card>
            <CardHeader title="Welcome back!" />
            <CardContent>
              {/* 📋 Use prep list features */}
              <Button onClick={() => createList()}>
                Create New Prep List
              </Button>
              
              {/* 📱 Use OCR features */}
              <Button onClick={() => scanDocument()}>
                Scan Document
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
```

### **Package Dependencies**
```json
// Main app package.json
{
  "dependencies": {
    "@prep-chef/ui-components": "workspace:*",
    "@prep-chef/auth": "workspace:*",
    "@prep-chef/features-prep-lists": "workspace:*",
    "@prep-chef/features-ocr": "workspace:*",
    "@prep-chef/features-settings": "workspace:*"
  }
}
```

## Integration States

### **State 1: Pure Design (Independent)**
- Packages work standalone
- No data persistence
- UI and interaction only
- Perfect for design iteration

### **State 2: Full Integration (Connected)**
- Packages share state
- Database persistence
- Real authentication
- Full business logic

## Commands

### **Development Workflow**
```bash
# 🎨 Design independently
./dev-packages.sh                    # Choose package to work on

# 🔨 Build for integration  
npm run build:packages               # Build all packages

# 🚀 Test full integration
npm run dev                          # Full app with all features

# 📦 Production build
npm run build                        # Build everything for production
```

### **Package-Specific Integration**
```bash
# Build specific package and test in main app
cd packages/ui-components && npm run build
cd ../.. && npm run dev

# Or build and watch for changes
npm run watch:packages               # Auto-rebuild on changes
npm run dev:app                      # Main app with hot reload
```

## Integration Architecture

```
┌─────────────────────────────────────┐
│           Main App (src/)           │
│  ┌─────────────────────────────────┐│
│  │        App.tsx (Orchestrator)   ││
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐││
│  │  │ UI  │ │Auth │ │Prep │ │ OCR │││
│  │  │Comp │ │     │ │List │ │     │││
│  │  └─────┘ └─────┘ └─────┘ └─────┘││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
           ↑ Imports from ↑
┌─────────────────────────────────────┐
│      Independent Packages          │
│ packages/ui-components/dist/        │
│ packages/auth/dist/                 │
│ packages/features-prep-lists/dist/  │
│ packages/features-ocr/dist/         │
│ packages/features-settings/dist/    │
└─────────────────────────────────────┘
```

## Benefits of This Architecture

### ✅ **Best of Both Worlds**
- **Independent**: Design and test packages separately
- **Integrated**: Full functionality when combined
- **Incremental**: Add features one package at a time
- **Maintainable**: Update packages without breaking others

### ✅ **Team Workflow**
```
Designer → Works on packages/ui-components/dev/
Frontend Dev → Works on individual package features  
Backend Dev → Integrates with src/App.tsx
Product Manager → Reviews both standalone and integrated versions
```

### ✅ **Deployment Strategy**
```
Development: Use standalone packages for rapid iteration
Staging: Use integrated app for full testing
Production: Deploy integrated app with all features
```
