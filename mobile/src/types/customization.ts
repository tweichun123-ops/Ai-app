export type LanguageOption = 'en-US' | 'ja-JP' | 'ko-KR';

export type AvatarTemplate =
  | 'kr_college'
  | 'jp_senior'
  | 'us_executive'
  | 'sunny_athlete'
  | 'artistic_musician'
  | 'gentle_researcher';

export type VoiceType = 'kr_soft' | 'jp_cool' | 'en_deep';

export type CustomizationProfile = {
  language: LanguageOption;
  template: AvatarTemplate;
  hairColor: 'black' | 'brown' | 'gold';
  bodyType: 'slim' | 'fit' | 'broad';
  warmth: number;
  initiative: number;
  humor: number;
  possessiveness: number;
  voice: VoiceType;
  nickname: string;
};

export const defaultProfile: CustomizationProfile = {
  language: 'en-US',
  template: 'kr_college',
  hairColor: 'black',
  bodyType: 'fit',
  warmth: 70,
  initiative: 65,
  humor: 55,
  possessiveness: 45,
  voice: 'kr_soft',
  nickname: '宝贝',
};
