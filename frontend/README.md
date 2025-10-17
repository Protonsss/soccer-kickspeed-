# KickSpeed Pro - Frontend

Modern, beautiful Next.js frontend for KickSpeed Pro.

## Features

- 🎨 Beautiful, modern UI with glass morphism effects
- 📱 Fully responsive design
- ⚡ Real-time analysis progress
- 📊 Interactive charts and visualizations
- 🎯 Goal placement heat maps
- 📈 Detailed metrics dashboard
- 🌙 Dark mode optimized

## Tech Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **TailwindCSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **Recharts**: Data visualization
- **Lucide Icons**: Beautiful icons

## Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Components

- `VideoUploader`: Drag & drop video upload
- `AnalysisResults`: Main results dashboard
- `MetricsOverview`: Quick metrics cards
- `SpeedChart`: Speed over time visualization
- `TrajectoryVisualization`: Ball path plot
- `GoalPlacement`: Shot placement heat map
- `DetailedMetrics`: Comprehensive metrics table

## Environment Variables

No environment variables required. Backend API URL is hardcoded to `http://localhost:8000`.

For production, update the API URL in components.

## Customization

### Colors
Edit `tailwind.config.ts` to change the color scheme.

### Animations
Modify Framer Motion settings in components for different animation styles.

