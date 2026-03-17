# iOS Closet Preview module (SwiftUI + MVVM)

This folder provides a production-style scaffold for the target UI:

- Left panel: closet list.
- Right panel: realtime try-on preview.
- States: idle / loading / success / failure.

## Integration steps

1. Add these files into your Xcode project target.
2. Pass real `accessToken` and `userId` after login.
3. Keep backend endpoint as:
   - `GET /api/users/{user_id}/closet/items?tab=all`
   - `POST /api/users/{user_id}/closet/try-on`

## Architecture

- `APIClient`: HTTP layer.
- `ClosetPreviewViewModel`: state + async actions.
- `ClosetPreviewView`: two-column visual layout with instant preview updates.

## Notes

- This module expects backend Bearer auth to be enabled.
- For iPhone portrait, you can switch from fixed split to stacked layout via size class.
