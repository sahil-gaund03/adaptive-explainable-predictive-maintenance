# Design System Specification: Palantir Foundry Dark Glassmorphism

An enterprise-grade UI design system engineered for Industrial AI platforms (Industry 4.0 / 5.0).

---

## 1. Color Palette

```
[ Canvas Dark Slate ]     #090d16 (Deep background)
[ Sidebar Slate ]          #0c1220 (Elevated navigation panel)
[ Card Surface ]           #121929 (Glassmorphism container)
[ Card Border ]            #1e293b (Subtle separation border)
[ Primary Accent (Cyan) ]  #38bdf8 (AI Guidance & Active links)
[ Status Emerald ]         #10b981 (Healthy / High confidence)
[ Status Amber ]           #f59e0b (Warning / Medium risk)
[ Status Ruby ]            #ef4444 (Critical / High risk)
```

---

## 2. Typography Hierarchy

- **Font Family**: `'Inter', -apple-system, BlinkMacSystemFont, sans-serif`
- **Page Titles**: `24px`, Bold (700), `#ffffff`
- **Section Headers**: `18px`, Semi-Bold (600), `#f1f5f9`
- **KPI Values**: `32px`, Extra-Bold (800), `#ffffff`
- **KPI Subtext**: `12px`, Medium (500), `#10b981` / `#64748b`
- **Body Text**: `14px`, Regular (400), `#cbd5e1`

---

## 3. Component Guidelines

### 3.1 Status Badges
- **Healthy**: `background-color: rgba(16, 185, 129, 0.12); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3);`
- **Warning**: `background-color: rgba(245, 158, 11, 0.12); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3);`
- **Critical**: `background-color: rgba(239, 68, 68, 0.12); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3);`

### 3.2 Action Buttons
- **Primary Operational Button**: Action-driven copy (*"Inspect Machine #17"*), full container width, accent background.
- **Secondary Action Button**: Outlined button (*"Generate Maintenance Report"*), subtle hover response.
