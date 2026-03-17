# Nexis Mobile (React Native + Expo + TypeScript scaffold)

This module implements the PRD-aligned mobile UI foundations:

1. Global design system + reusable components.
2. Login screen.
3. Subscription screen.
4. Wardrobe screen with right-side realtime preview panel pattern.
5. Outfit detail screen with bottom sheet style panel.

## Suggested branch split

- `feat/mobile-theme-foundation`
- `feat/mobile-auth-login`
- `feat/mobile-subscription`
- `feat/mobile-wardrobe`
- `feat/mobile-outfit-detail`

## Integration

- Plug into an Expo Router or React Navigation host app.
- Replace placeholder APIs in `services/api.ts` style calls with real backend endpoints.
- Replace placeholder images with CDN assets.

## Ideal-type onboarding wizard (implemented)

- Step 1: language selection
- Step 2: avatar template + light appearance customization
- Step 3: personality sliders
- Step 4: voice + nickname
- Step 5: generate first romantic photo then enter wardrobe

The wizard includes a right-side realtime preview panel to reinforce ownership and emotional projection.
