import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { LoginScreen } from '../screens/LoginScreen';
import { SubscriptionScreen } from '../screens/SubscriptionScreen';
import { CustomizationWizardScreen } from '../screens/CustomizationWizardScreen';
import { WardrobeScreen } from '../screens/WardrobeScreen';
import { OutfitDetailScreen } from '../screens/OutfitDetailScreen';
import { RootStackParamList } from '../types/navigation';

const Stack = createNativeStackNavigator<RootStackParamList>();

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }} initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Subscription" component={SubscriptionScreen} />
        <Stack.Screen name="CustomizationWizard" component={CustomizationWizardScreen} />
        <Stack.Screen name="Wardrobe" component={WardrobeScreen} />
        <Stack.Screen name="OutfitDetail" component={OutfitDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
