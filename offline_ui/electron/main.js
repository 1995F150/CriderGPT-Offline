const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess = null;
let splash;

function createSplash() {
  splash = new BrowserWindow({
    width: 480,
    height: 300,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
  });
  splash.loadFile(path.join(__dirname, 'splash.html'));
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    icon: path.join(__dirname, '..', '..', 'assets', 'logo.png')
  });

  const indexPath = path.join(__dirname, '..', '..', 'dist', 'index.html');
  if (require('fs').existsSync(indexPath)) {
    mainWindow.loadFile(indexPath);
  } else {
    // during dev Vite runs on localhost:5173
    mainWindow.loadURL('http://localhost:5173');
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startBackendIfNeeded() {
  // prefer a bundled backend executable if present
  const exePath = path.join(__dirname, '..', '..', 'dist-backend', 'CriderGPT_Backend.exe');
  if (require('fs').existsSync(exePath)) {
    backendProcess = spawn(exePath, [], { detached: true, stdio: 'ignore' });
    backendProcess.unref();
  } else {
    // fallback to launching python script if Python is available
    const py = process.platform === 'win32' ? 'python' : 'python3';
    const script = path.join(__dirname, '..', '..', 'main.py');
    if (require('fs').existsSync(script)) {
      backendProcess = spawn(py, [script], { stdio: 'ignore', detached: true });
      backendProcess.unref();
    }
  }
}

app.on('ready', () => {
  createSplash();
  startBackendIfNeeded();
  setTimeout(() => {
    createWindow();
    if (splash) splash.close();
  }, 1200);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', () => {
  if (backendProcess) {
    try { process.kill(-backendProcess.pid); } catch(e){}
  }
});
