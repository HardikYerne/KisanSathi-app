# KisanSathi AI — React Native + Expo SDK 57 frontend prototype

A mobile-first TypeScript frontend prototype for an AI Farming Assistant. Includes a farmer-themed home dashboard, language picker, crop-photo selection/camera flow, AI voice-assistant UI, farm planner, task check-offs, and profile/preferences.

## Run it on your phone (recommended)

1. Install **Node.js LTS** on your computer: https://nodejs.org/
2. Extract this ZIP and open a terminal in the `farmer-ai-mobile` folder.
3. Install dependencies:

   ```bash
   npm install
   ```

4. Start Expo:

   ```bash
   npx expo start
   ```

5. Install the current **Expo Go** app on your Android phone. Scan the QR code shown in the terminal/browser while your phone and computer are on the same Wi-Fi network. Expo Go SDK support can change; if you see an SDK compatibility error, use the compatible Expo Go build or a development build.

If the LAN connection does not work, try:

```bash
npx expo start --tunnel
```

## Run in an emulator

- Android: install Android Studio and configure an Android emulator, then run `npm run android`.
- Web preview (useful for a quick look; camera APIs may differ): run `npm run web`.

## What works in this prototype

- Bottom-tab navigation between Home, Scan, Ask AI, Planner, and Profile.
- Language selection (Marathi, Hindi, English, Gujarati, Punjabi, Bengali, Tamil, Telugu). The home greeting switches for Marathi, Hindi, and English; the selection UI works for all listed languages.
- Select a crop image from the gallery or take a photo (device permissions required).
- AI assistant screen with a listening-state toggle and example question prompts.
- Check off planner tasks, reset tasks, and toggle reminder preference.
- Farmer imagery and responsive mobile layout.

## Not connected yet

- Real speech-to-text or text-to-speech.
- LLM responses, plant recognition, disease segmentation/classification, fertilizer calculations, authentication, weather, market prices, push notifications, or persistent backend data.
- The scan result is deliberately a demo notice; it does not make agricultural diagnoses.

## Suggested next integration

Create a Python FastAPI backend with `/api/v1/auth`, `/api/v1/scans`, `/api/v1/assistant`, `/api/v1/weather`, `/api/v1/crop-plans`, and `/api/v1/market-prices`. Configure an API base URL using an environment variable and replace demo alerts with typed API calls. Do not show a fertilizer or pesticide dosage unless it is supported by verified crop/region/soil guidance.


## Updated frontend screens
- Farmer services cards for nearby seed/fertilizer shops, government schemes, and land/property records.
- Signup/login UI with name, email/phone, password, and address fields (street/locality, village/town, district, state, PIN code).
- GPS permission entry point and address summary UI.

These are frontend interactions/demo placeholders. Live maps require a Maps/Places provider and Expo Location integration; authentication/address persistence requires connecting to the FastAPI backend. The GPS button currently explains the integration point and does not request device coordinates yet.
