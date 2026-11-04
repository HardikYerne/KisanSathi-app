import React, { useState } from 'react';
import {
  Alert, Image, ImageBackground, Modal, Pressable, ScrollView, StatusBar,
  StyleSheet, Text, View, SafeAreaView, Switch, TextInput,
} from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';

type Tab = 'Home' | 'Scan' | 'Ask AI' | 'Planner' | 'Profile';
const GREEN = '#176B42';
const DEEP = '#104B31';
const MINT = '#E8F4E8';
const BG = '#F5F7F1';
const INK = '#1D3025';
const MUTED = '#758276';
const languages = ['मराठी', 'हिन्दी', 'English', 'ગુજરાતી', 'ਪੰਜਾਬੀ', 'বাংলা', 'தமிழ்', 'తెలుగు'];
const copy: Record<string, { greeting: string; subtitle: string; ask: string; scan: string; crops: string; weather: string; planner: string }> = {
  'मराठी': { greeting: 'नमस्कार, शेतकरी मित्रा!', subtitle: 'आज शेतीसाठी काय मदत हवी?', ask: 'AI शेती सहाय्यकाला विचारा', scan: 'पीक तपासा', crops: 'माझी पिके', weather: 'हवामान', planner: 'शेती नियोजन' },
  'हिन्दी': { greeting: 'नमस्ते, किसान मित्र!', subtitle: 'आज खेती में क्या मदद चाहिए?', ask: 'AI किसान साथी से पूछें', scan: 'फसल जाँचें', crops: 'मेरी फसलें', weather: 'मौसम', planner: 'खेती की योजना' },
  English: { greeting: 'Hello, farmer friend!', subtitle: 'How can we help your farm today?', ask: 'Ask your AI farming assistant', scan: 'Scan a crop', crops: 'My crops', weather: 'Weather', planner: 'Farm planner' },
};

function Card({ children, style }: { children: React.ReactNode; style?: any }) {
  return <View style={[styles.card, style]}>{children}</View>;
}
function SectionTitle({ title, action, onAction }: { title: string; action?: string; onAction?: () => void }) {
  return <View style={styles.sectionHead}><Text style={styles.sectionTitle}>{title}</Text>{action ? <Text onPress={onAction} style={styles.link}>{action}</Text> : null}</View>;
}
function IconTile({ icon, color = GREEN, background = MINT, size = 23 }: { icon: keyof typeof Ionicons.glyphMap; color?: string; background?: string; size?: number }) {
  return <View style={[styles.iconTile, { backgroundColor: background }]}><Ionicons name={icon} size={size} color={color} /></View>;
}

export default function App() {
  const [tab, setTab] = useState<Tab>('Home');
  const [language, setLanguage] = useState('मराठी');
  const [languageModal, setLanguageModal] = useState(false);
  const [listening, setListening] = useState(false);
  const [doneTasks, setDoneTasks] = useState<number[]>([0]);
  const [notifications, setNotifications] = useState(true);
  const [pickedImage, setPickedImage] = useState<string | null>(null);
  const [scanning, setScanning] = useState(false);
  const [authVisible, setAuthVisible] = useState(false);
  const [authMode, setAuthMode] = useState<'Sign up' | 'Login'>('Sign up');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [address, setAddress] = useState('');
  const [village, setVillage] = useState('');
  const [district, setDistrict] = useState('');
  const [stateName, setStateName] = useState('Maharashtra');
  const [pincode, setPincode] = useState('');
  const [locationLabel, setLocationLabel] = useState('Add your farm address');
  const t = copy[language] || copy.English;

  const chooseImage = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) {
      Alert.alert('Photo access needed', 'Allow photo-library access to select a crop image for this demo.');
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'], allowsEditing: true, quality: 0.85 });
    if (!result.canceled && result.assets[0]) {
      setPickedImage(result.assets[0].uri);
      setScanning(false);
      setTab('Scan');
    }
  };
  const takePhoto = async () => {
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (!permission.granted) {
      Alert.alert('Camera access needed', 'Allow camera access to take a crop photo.');
      return;
    }
    const result = await ImagePicker.launchCameraAsync({ allowsEditing: true, quality: 0.85 });
    if (!result.canceled && result.assets[0]) {
      setPickedImage(result.assets[0].uri);
      setScanning(false);
      setTab('Scan');
    }
  };
  const startVoice = () => {
    setListening(v => !v);
    if (!listening) Alert.alert('AI voice demo', `Voice interaction UI is ready for ${language}. Connect speech-to-text and text-to-speech services to enable real conversations.`);
  };
  const runDemoScan = () => {
    if (!pickedImage) {
      Alert.alert('Add a crop photo', 'Take a photo or choose one from your gallery to preview the scan-result screen.');
      return;
    }
    setScanning(true);
    setTimeout(() => {
      setScanning(false);
      Alert.alert('Demo result only', 'The photo is displayed successfully. Real crop and disease predictions will appear after the vision model API is connected.');
    }, 700);
  };
  const quickAction = (name: string) => {
    if (name === 'Scan') { setTab('Scan'); return; }
    if (name === 'AI Assistant') { setTab('Ask AI'); return; }
    if (name === 'Farm planner') { setTab('Planner'); return; }
    if (name === 'Nearby seed & fertilizer shops') { Alert.alert('Nearby agriculture shops', `Location: ${locationLabel}\n\nThe live map will show nearby seed shops, fertilizer dealers, nurseries, distance, and directions after Maps/Places API integration.`); return; }
    if (name === 'Government schemes') { Alert.alert('Government schemes', 'Browse farmer schemes, eligibility, documents, deadlines, and official application links. Scheme data must be sourced and periodically verified from official portals.'); return; }
    if (name === 'Land & property records') { Alert.alert('Land & property information', 'Find official services for 7/12, 8A, property cards, mutation records, and land maps. Maharashtra portal: https://bhulekh.mahabhumi.gov.in/'); return; }
    Alert.alert(name, 'This screen is represented in the frontend demo. Live data will require backend and data-source integration.');
  };

  const renderHome = () => <>
    <View style={styles.topRow}>
      <View style={styles.brandRow}><View style={styles.logo}><MaterialCommunityIcons name="sprout" size={25} color="#FFFFFF" /></View><View><Text style={styles.brand}>Kisan<Text style={{ color: '#E5A83C' }}>Sathi</Text></Text><Text style={styles.brandSub}>AI FARMING ASSISTANT</Text></View></View>
      <Pressable style={styles.roundButton} onPress={() => Alert.alert('Notifications', 'Your farming reminders and alerts will appear here.')}><Ionicons name="notifications-outline" size={22} color={INK} /><View style={styles.notificationDot} /></Pressable>
    </View>
    <Pressable style={styles.languagePill} onPress={() => setLanguageModal(true)}><Ionicons name="globe-outline" size={16} color={GREEN} /><Text style={styles.languagePillText}>{language}</Text><Ionicons name="chevron-down" size={15} color={GREEN} /></Pressable>
    <View style={styles.hero}>
      <View style={styles.heroCopy}>
        <Text style={styles.eyebrow}>YOUR FARMING COMPANION</Text>
        <Text style={styles.heroTitle}>{t.greeting}</Text>
        <Text style={styles.heroSub}>{t.subtitle}</Text>
        <Pressable style={styles.heroButton} onPress={() => setTab('Ask AI')}><Ionicons name="chatbubble-ellipses" size={17} color={GREEN} /><Text style={styles.heroButtonText}>{t.ask}</Text><Ionicons name="arrow-forward" size={16} color={GREEN} /></Pressable>
      </View>
      <Image source={require('./assets/farmer-character.png')} style={styles.farmerImage} resizeMode="cover" />
      <View style={styles.heroLeaf}><MaterialCommunityIcons name="leaf" size={18} color="#FFFFFF" /></View>
    </View>
    <View style={styles.weatherStrip}>
      <View style={styles.weatherIcon}><Ionicons name="partly-sunny" size={29} color="#E9A92F" /></View>
      <View style={{ flex: 1 }}><Text style={styles.weatherPlace}>YOUR FARM · DEMO WEATHER</Text><Text style={styles.weatherTemp}>28° <Text style={styles.weatherDesc}>Partly cloudy</Text></Text><Text style={styles.weatherHint}>Check local forecast before irrigation</Text></View>
      <Ionicons name="chevron-forward" size={18} color={MUTED} />
    </View>
    <SectionTitle title="Quick actions" />
    <View style={styles.actionGrid}>
      <Pressable style={styles.actionItem} onPress={() => quickAction('Scan')}><IconTile icon="scan-outline" background="#E1F2E6" /><Text style={styles.actionLabel}>{t.scan}</Text></Pressable>
      <Pressable style={styles.actionItem} onPress={() => quickAction('My crops')}><IconTile icon="leaf-outline" background="#F4EBD4" color="#9D7627" /><Text style={styles.actionLabel}>{t.crops}</Text></Pressable>
      <Pressable style={styles.actionItem} onPress={() => quickAction('Weather')}><IconTile icon="cloudy-outline" background="#E0EEF8" color="#3778A5" /><Text style={styles.actionLabel}>{t.weather}</Text></Pressable>
      <Pressable style={styles.actionItem} onPress={() => quickAction('Farm planner')}><IconTile icon="calendar-outline" background="#F7E6DF" color="#B96A44" /><Text style={styles.actionLabel}>{t.planner}</Text></Pressable>
    </View>
    <SectionTitle title="Farmer services" />
    <View style={styles.toolList}>
      {[['Nearby seed & fertilizer shops', 'Map, distance, contact and directions', 'location-outline'], ['Government schemes', 'Benefits, eligibility and official links', 'ribbon-outline'], ['Land & property records', '7/12, 8A, property card and land maps', 'document-text-outline']].map(([name, sub, icon]) => <Pressable key={name} style={styles.toolRow} onPress={() => quickAction(name)}><IconTile icon={icon as any} size={20} /><View style={{ flex: 1 }}><Text style={styles.toolName}>{name}</Text><Text style={styles.toolSub}>{sub}</Text></View><Ionicons name="chevron-forward" size={18} color={MUTED} /></Pressable>)}
    </View>
    <Pressable style={styles.locationBanner} onPress={() => setAuthVisible(true)}><Ionicons name="navigate-circle-outline" size={27} color={GREEN} /><View style={{ flex: 1 }}><Text style={styles.toolName}>{locationLabel}</Text><Text style={styles.toolSub}>Add village, district, state and PIN code to personalize nearby services.</Text></View><Ionicons name="chevron-forward" size={18} color={MUTED} /></Pressable>
    <SectionTitle title="Your farm at a glance" action="View all" onAction={() => quickAction('My farm')} />
    <View style={styles.statsRow}><Card style={styles.statCard}><IconTile icon="grid-outline" size={19} /><Text style={styles.statNumber}>02</Text><Text style={styles.statLabel}>Demo plots</Text></Card><Card style={styles.statCard}><IconTile icon="leaf" size={19} background="#F4EBD4" color="#9D7627" /><Text style={styles.statNumber}>03</Text><Text style={styles.statLabel}>Crop records</Text></Card><Card style={styles.statCard}><IconTile icon="checkmark-circle-outline" size={19} background="#E0EEF8" color="#3778A5" /><Text style={styles.statNumber}>04</Text><Text style={styles.statLabel}>Tasks this week</Text></Card></View>
    <SectionTitle title="This week on your farm" action="Open planner" onAction={() => setTab('Planner')} />
    <Card style={{ marginBottom: 20 }}>
      {[['Water check for tomato plot', 'Today · Morning', 'water-outline'], ['Review crop health', 'Tomorrow · 9:00 AM', 'leaf-outline'], ['Check market prices', 'Friday · Anytime', 'trending-up-outline']].map((task, i) => <Pressable key={task[0]} style={styles.taskRow} onPress={() => setDoneTasks(old => old.includes(i) ? old.filter(x => x !== i) : [...old, i])}><View style={[styles.taskCheck, doneTasks.includes(i) && styles.taskCheckDone]}>{doneTasks.includes(i) ? <Ionicons name="checkmark" size={14} color="#FFF" /> : null}</View><View style={{ flex: 1 }}><Text style={[styles.taskTitle, doneTasks.includes(i) && styles.taskDoneText]}>{task[0]}</Text><Text style={styles.taskTime}>{task[1]}</Text></View><Ionicons name={task[2] as any} size={20} color={MUTED} /></Pressable>)}
    </Card>
  </>;

  const renderScan = () => <>
    <View style={styles.pageHeader}><Text style={styles.pageTitle}>Crop health scan</Text><Text style={styles.pageSubtitle}>Take a clear photo of a leaf or plant.</Text></View>
    <Pressable style={styles.scanPreview} onPress={chooseImage}>
      {pickedImage ? <Image source={{ uri: pickedImage }} style={styles.selectedPhoto} resizeMode="cover" /> : <><View style={styles.scanCorners}><View style={styles.cornerTL} /><View style={styles.cornerTR} /><View style={styles.cornerBL} /><View style={styles.cornerBR} /></View><View style={styles.scanPlaceholder}><Ionicons name="leaf-outline" size={50} color={GREEN} /><Text style={styles.scanPlaceholderTitle}>Your crop photo goes here</Text><Text style={styles.scanPlaceholderText}>Frame the affected leaf in good light</Text></View></>}
    </Pressable>
    <View style={styles.twoButtons}><Pressable style={styles.primaryButton} onPress={takePhoto}><Ionicons name="camera-outline" size={19} color="#FFF" /><Text style={styles.primaryButtonText}>Take photo</Text></Pressable><Pressable style={styles.secondaryButton} onPress={chooseImage}><Ionicons name="images-outline" size={19} color={GREEN} /><Text style={styles.secondaryButtonText}>Choose image</Text></Pressable></View>
    <Pressable style={[styles.primaryButton, styles.fullButton, !pickedImage && { opacity: 0.65 }]} onPress={runDemoScan}><Ionicons name="scan" size={19} color="#FFF" /><Text style={styles.primaryButtonText}>{scanning ? 'Preparing preview…' : 'Analyze crop (demo)'}</Text></Pressable>
    <View style={styles.infoBox}><Ionicons name="information-circle-outline" size={21} color={GREEN} /><Text style={styles.infoText}>This test build previews the scan flow only. It does not diagnose diseases until a trained vision model is connected.</Text></View>
    <SectionTitle title="Tips for a useful scan" />
    {['Use natural daylight and avoid strong shadows.', 'Keep the affected area in focus.', 'Photograph the whole plant if symptoms are widespread.', 'Add crop name and growth stage for better context.'].map((item, i) => <View key={item} style={styles.tipRow}><View style={styles.tipNumber}><Text style={styles.tipNumberText}>{i + 1}</Text></View><Text style={styles.tipText}>{item}</Text></View>)}
  </>;

  const renderAI = () => <>
    <View style={styles.pageHeader}><Text style={styles.pageTitle}>AI KisanSathi</Text><Text style={styles.pageSubtitle}>Talk about your crops in your language.</Text></View>
    <View style={styles.aiHero}><Image source={require('./assets/farmer-character.png')} style={styles.aiFarmer} resizeMode="cover" /><Text style={styles.aiGreeting}>{listening ? 'I’m ready to listen…' : 'Namaskar, farmer friend!'}</Text><Text style={styles.aiHint}>{listening ? `Listening state · ${language}` : 'Tap the microphone to start a voice session'}</Text><Pressable onPress={startVoice} style={[styles.micButton, listening && styles.micButtonActive]}><Ionicons name={listening ? 'stop' : 'mic'} size={29} color="#FFF" /></Pressable><Text style={styles.micCaption}>{listening ? 'Tap to stop' : 'Tap to speak'}</Text><Pressable style={styles.languageSelectWide} onPress={() => setLanguageModal(true)}><Ionicons name="globe-outline" size={17} color={GREEN} /><Text style={styles.languageSelectText}>Reply language: {language}</Text><Ionicons name="chevron-down" size={17} color={GREEN} /></Pressable></View>
    <SectionTitle title="Try asking" />
    {['What is wrong with my tomato plant?', 'When should I water my crop?', 'Explain fertilizer for my soil', 'What should I plant this season?'].map((q, i) => <Pressable key={q} style={styles.promptRow} onPress={() => Alert.alert('Prompt preview', `“${q}”\n\nConnect the AI backend to generate a verified answer in ${language}.`)}><View style={styles.promptIcon}><Ionicons name={['leaf-outline', 'water-outline', 'flask-outline', 'sunny-outline'][i] as any} size={19} color={GREEN} /></View><Text style={styles.promptText}>{q}</Text><Ionicons name="arrow-up-outline" size={18} color={MUTED} /></Pressable>)}
    <View style={styles.infoBox}><Ionicons name="language-outline" size={21} color={GREEN} /><Text style={styles.infoText}>Language selection is interactive. Real speech recognition and spoken AI responses need service integration.</Text></View>
  </>;

  const renderPlanner = () => <>
    <View style={styles.pageHeader}><Text style={styles.pageTitle}>Farm planner</Text><Text style={styles.pageSubtitle}>Keep important farm work in one place.</Text></View>
    <View style={styles.planBanner}><View style={{ flex: 1 }}><Text style={styles.planEyebrow}>YOUR NEXT STEP</Text><Text style={styles.planTitle}>A little planning goes a long way.</Text><Text style={styles.planBody}>Set reminders for watering, crop checks, and farm activities.</Text></View><MaterialCommunityIcons name="calendar-check" size={53} color="#C7E7C7" /></View>
    <SectionTitle title="Upcoming tasks" action="Reset" onAction={() => setDoneTasks([])} />
    <Card>{[['Water check for tomato plot', 'Today · Morning', 'water-outline'], ['Review crop health', 'Tomorrow · 9:00 AM', 'leaf-outline'], ['Check market prices', 'Friday · Anytime', 'trending-up-outline'], ['Prepare weekly crop notes', 'Sunday · Evening', 'document-text-outline']].map((task, i) => <Pressable key={task[0]} style={styles.plannerTask} onPress={() => setDoneTasks(old => old.includes(i) ? old.filter(x => x !== i) : [...old, i])}><View style={[styles.taskCheck, doneTasks.includes(i) && styles.taskCheckDone]}>{doneTasks.includes(i) ? <Ionicons name="checkmark" size={14} color="#FFF" /> : null}</View><View style={{ flex: 1 }}><Text style={styles.taskTitle}>{task[0]}</Text><Text style={styles.taskTime}>{task[1]}</Text></View><Ionicons name={task[2] as any} size={21} color={GREEN} /></Pressable>)}</Card>
    <SectionTitle title="Farm tools" />
    <View style={styles.toolList}>{[['Fertilizer guide', 'flask-outline'], ['Weather & irrigation', 'cloud-outline'], ['Market prices', 'trending-up-outline'], ['Crop calendar', 'calendar-outline']].map(([name, icon]) => <Pressable key={name} style={styles.toolRow} onPress={() => quickAction(name)}><IconTile icon={icon as any} size={20} /><Text style={styles.toolName}>{name}</Text><Ionicons name="chevron-forward" size={18} color={MUTED} /></Pressable>)}</View>
    <View style={styles.infoBox}><Ionicons name="shield-checkmark-outline" size={21} color={GREEN} /><Text style={styles.infoText}>Fertilizer quantities and treatment schedules must be calculated from verified crop, soil, location, and product information.</Text></View>
  </>;

  const renderProfile = () => <>
    <View style={styles.pageHeader}><Text style={styles.pageTitle}>Your profile</Text><Text style={styles.pageSubtitle}>Set up the app for your farm.</Text></View>
    <Card style={styles.profileCard}><Image source={require('./assets/farmer-character.png')} style={styles.profileAvatar} /><Text style={styles.profileName}>Farmer profile</Text><Text style={styles.profileDetail}>Demo account · {locationLabel}</Text><Pressable style={styles.secondaryButton} onPress={() => { setAuthMode('Sign up'); setAuthVisible(true); }}><Ionicons name="person-add-outline" size={18} color={GREEN} /><Text style={styles.secondaryButtonText}>Set up account</Text></Pressable></Card>
    <SectionTitle title="Preferences" />
    <View style={styles.toolList}>
      <Pressable style={styles.toolRow} onPress={() => setAuthVisible(true)}><IconTile icon="location-outline" size={20} /><View style={{ flex: 1 }}><Text style={styles.toolName}>Farm address & location</Text><Text style={styles.toolSub}>{locationLabel}</Text></View><Ionicons name="chevron-forward" size={18} color={MUTED} /></Pressable>
      <Pressable style={styles.toolRow} onPress={() => setLanguageModal(true)}><IconTile icon="globe-outline" size={20} /><View style={{ flex: 1 }}><Text style={styles.toolName}>App language</Text><Text style={styles.toolSub}>{language}</Text></View><Ionicons name="chevron-forward" size={18} color={MUTED} /></Pressable>
      <View style={styles.toolRow}><IconTile icon="notifications-outline" size={20} /><View style={{ flex: 1 }}><Text style={styles.toolName}>Farm reminders</Text><Text style={styles.toolSub}>Task and crop-care notifications</Text></View><Switch value={notifications} onValueChange={setNotifications} trackColor={{ false: '#D9E0D7', true: '#9BCDAA' }} thumbColor={notifications ? GREEN : '#FFFFFF'} /></View>
      <Pressable style={styles.toolRow} onPress={() => Alert.alert('Privacy', 'Your data policy and consent controls will be added before production release.')}><IconTile icon="shield-checkmark-outline" size={20} /><Text style={styles.toolName}>Privacy & data</Text><Ionicons name="chevron-forward" size={18} color={MUTED} /></Pressable>
      <Pressable style={styles.toolRow} onPress={() => Alert.alert('About KisanSathi', 'Interactive frontend prototype · AI and live data are not connected yet.')}><IconTile icon="information-circle-outline" size={20} /><Text style={styles.toolName}>About this app</Text><Ionicons name="chevron-forward" size={18} color={MUTED} /></Pressable>
    </View>
    <Text style={styles.version}>KisanSathi AI · Frontend prototype v0.1</Text>
  </>;

  const renderContent = () => {
    switch (tab) {
      case 'Home': return renderHome();
      case 'Scan': return renderScan();
      case 'Ask AI': return renderAI();
      case 'Planner': return renderPlanner();
      case 'Profile': return renderProfile();
    }
  };

  const tabs: { name: Tab; icon: keyof typeof Ionicons.glyphMap; activeIcon: keyof typeof Ionicons.glyphMap }[] = [
    { name: 'Home', icon: 'home-outline', activeIcon: 'home' },
    { name: 'Scan', icon: 'scan-outline', activeIcon: 'scan' },
    { name: 'Ask AI', icon: 'chatbubble-ellipses-outline', activeIcon: 'chatbubble-ellipses' },
    { name: 'Planner', icon: 'calendar-outline', activeIcon: 'calendar' },
    { name: 'Profile', icon: 'person-circle-outline', activeIcon: 'person-circle' },
  ];

  return <SafeAreaView style={styles.safe}><StatusBar barStyle="dark-content" backgroundColor={BG} /><View style={styles.appShell}><ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>{renderContent()}</ScrollView><View style={styles.tabBar}>{tabs.map(item => { const active = tab === item.name; return <Pressable key={item.name} style={styles.tabItem} onPress={() => setTab(item.name)}><View style={[styles.tabIconWrap, active && styles.tabIconActive]}><Ionicons name={active ? item.activeIcon : item.icon} size={21} color={active ? '#FFFFFF' : MUTED} /></View><Text style={[styles.tabLabel, active && styles.tabLabelActive]}>{item.name}</Text></Pressable>; })}</View></View>
    <Modal visible={authVisible} transparent animationType="slide" onRequestClose={() => setAuthVisible(false)}><View style={styles.modalScrim}><View style={styles.authSheet}><View style={styles.sheetHandle} /><ScrollView showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled"><Text style={styles.sheetTitle}>{authMode === 'Sign up' ? 'Create your farmer account' : 'Welcome back'}</Text><Text style={styles.sheetSubtitle}>Your address helps personalize nearby shops, local schemes and farm information.</Text><View style={styles.authSwitch}><Pressable style={[styles.authModeButton, authMode === 'Sign up' && styles.authModeActive]} onPress={() => setAuthMode('Sign up')}><Text style={[styles.authModeText, authMode === 'Sign up' && styles.authModeTextActive]}>Sign up</Text></Pressable><Pressable style={[styles.authModeButton, authMode === 'Login' && styles.authModeActive]} onPress={() => setAuthMode('Login')}><Text style={[styles.authModeText, authMode === 'Login' && styles.authModeTextActive]}>Login</Text></Pressable></View>{authMode === 'Sign up' ? <><Text style={styles.fieldLabel}>Full name</Text><TextInput value={fullName} onChangeText={setFullName} placeholder="Enter your name" style={styles.textField} /><Text style={styles.fieldLabel}>Mobile number</Text><TextInput value={phone} onChangeText={setPhone} placeholder="e.g. +91 98765 43210" keyboardType="phone-pad" style={styles.textField} /></> : null}<Text style={styles.fieldLabel}>Email (optional if phone is used)</Text><TextInput value={email} onChangeText={setEmail} placeholder="you@example.com" keyboardType="email-address" autoCapitalize="none" style={styles.textField} /><Text style={styles.fieldLabel}>Password</Text><TextInput value={password} onChangeText={setPassword} placeholder="At least 8 characters" secureTextEntry style={styles.textField} />{authMode === 'Sign up' ? <><Text style={styles.formSection}>Farm / home address</Text><Text style={styles.fieldLabel}>House, street or locality</Text><TextInput value={address} onChangeText={setAddress} placeholder="House number, street, locality" style={styles.textField} /><Text style={styles.fieldLabel}>Village / town</Text><TextInput value={village} onChangeText={setVillage} placeholder="Village or town" style={styles.textField} /><View style={styles.fieldRow}><View style={{ flex: 1 }}><Text style={styles.fieldLabel}>District</Text><TextInput value={district} onChangeText={setDistrict} placeholder="District" style={styles.textField} /></View><View style={{ flex: 1 }}><Text style={styles.fieldLabel}>State</Text><TextInput value={stateName} onChangeText={setStateName} placeholder="State" style={styles.textField} /></View></View><Text style={styles.fieldLabel}>PIN code</Text><TextInput value={pincode} onChangeText={setPincode} placeholder="6-digit PIN code" keyboardType="number-pad" maxLength={6} style={styles.textField} /><Pressable style={styles.secondaryButton} onPress={() => Alert.alert('Location permission', 'In the connected build, this button will request permission to use GPS and fill coordinates/address where supported. You can also enter your address manually.')}><Ionicons name="locate-outline" size={18} color={GREEN} /><Text style={styles.secondaryButtonText}>Use my current location (GPS)</Text></Pressable></> : null}<Pressable style={[styles.primaryButton, { marginTop: 16, marginBottom: 10 }]} onPress={() => { if (authMode === 'Sign up' && (!fullName.trim() || (!email.trim() && !phone.trim()) || password.length < 8)) { Alert.alert('Complete required fields', 'Enter your name, a phone number or email, and a password with at least 8 characters.'); return; } if (authMode === 'Sign up' && (address || village || district || stateName || pincode)) setLocationLabel([address, village, district, stateName, pincode].filter(Boolean).join(', ')); Alert.alert('Frontend demo', 'Form interaction works, but account creation and address storage require connecting these fields to the FastAPI backend.'); setAuthVisible(false); }}><Text style={styles.primaryButtonText}>{authMode === 'Sign up' ? 'Create account' : 'Login'}</Text></Pressable><Pressable onPress={() => setAuthVisible(false)} style={{ padding: 12, alignItems: 'center' }}><Text style={styles.link}>Close</Text></Pressable></ScrollView></View></View></Modal>
    <Modal visible={languageModal} transparent animationType="slide" onRequestClose={() => setLanguageModal(false)}><Pressable style={styles.modalScrim} onPress={() => setLanguageModal(false)}><Pressable style={styles.languageSheet} onPress={() => {}}><View style={styles.sheetHandle} /><Text style={styles.sheetTitle}>Choose your language</Text><Text style={styles.sheetSubtitle}>The assistant will use this language in the interface.</Text>{languages.map(lang => <Pressable key={lang} style={styles.languageOption} onPress={() => { setLanguage(lang); setLanguageModal(false); }}><Text style={[styles.languageOptionText, language === lang && { color: GREEN, fontWeight: '700' }]}>{lang}</Text>{language === lang ? <Ionicons name="checkmark-circle" size={21} color={GREEN} /> : <View style={styles.radioEmpty} />}</Pressable>)}</Pressable></Pressable></Modal>
  </SafeAreaView>;
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: BG }, appShell: { flex: 1 }, scrollContent: { paddingHorizontal: 20, paddingTop: 10, paddingBottom: 28 },
  topRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 13 }, brandRow: { flexDirection: 'row', alignItems: 'center', gap: 10 }, logo: { width: 44, height: 44, borderRadius: 15, backgroundColor: GREEN, alignItems: 'center', justifyContent: 'center' }, brand: { fontSize: 22, fontWeight: '800', color: DEEP, letterSpacing: -0.6 }, brandSub: { color: MUTED, fontSize: 8, letterSpacing: 1.6, fontWeight: '700', marginTop: 1 }, roundButton: { width: 43, height: 43, borderRadius: 15, backgroundColor: '#FFFFFF', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: '#E7ECE3' }, notificationDot: { width: 7, height: 7, borderRadius: 4, backgroundColor: '#D96B48', position: 'absolute', right: 10, top: 9 },
  languagePill: { alignSelf: 'flex-start', flexDirection: 'row', alignItems: 'center', gap: 7, paddingHorizontal: 12, paddingVertical: 8, backgroundColor: '#FFFFFF', borderRadius: 30, borderWidth: 1, borderColor: '#E3EAE0', marginBottom: 15 }, languagePillText: { fontSize: 12, color: GREEN, fontWeight: '700' },
  hero: { minHeight: 202, backgroundColor: '#DCEED9', borderRadius: 25, overflow: 'hidden', flexDirection: 'row', position: 'relative', marginBottom: 14 }, heroCopy: { flex: 1, padding: 17, paddingRight: 2, justifyContent: 'center', zIndex: 2 }, eyebrow: { fontSize: 8, letterSpacing: 1.1, color: GREEN, fontWeight: '800', marginBottom: 8 }, heroTitle: { color: DEEP, fontWeight: '800', fontSize: 21, lineHeight: 26, maxWidth: 205 }, heroSub: { color: '#476650', fontSize: 12, lineHeight: 17, marginTop: 5, maxWidth: 175 }, heroButton: { flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: '#FFFFFF', paddingHorizontal: 11, paddingVertical: 10, borderRadius: 13, alignSelf: 'flex-start', marginTop: 14 }, heroButtonText: { color: GREEN, fontWeight: '700', fontSize: 10 }, farmerImage: { width: '42%', height: '100%', position: 'absolute', right: -1, bottom: 0 }, heroLeaf: { position: 'absolute', right: 12, top: 12, width: 31, height: 31, borderRadius: 11, backgroundColor: GREEN, alignItems: 'center', justifyContent: 'center' },
  weatherStrip: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFFFFF', borderRadius: 18, padding: 13, gap: 12, marginBottom: 24, borderWidth: 1, borderColor: '#E8EDE4' }, weatherIcon: { width: 51, height: 51, borderRadius: 16, backgroundColor: '#FFF3D7', alignItems: 'center', justifyContent: 'center' }, weatherPlace: { fontSize: 9, letterSpacing: 0.6, color: MUTED, fontWeight: '800' }, weatherTemp: { color: INK, fontWeight: '800', fontSize: 20, marginTop: 1 }, weatherDesc: { fontSize: 12, fontWeight: '500', color: MUTED }, weatherHint: { fontSize: 10, color: MUTED, marginTop: 1 },
  sectionHead: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 13, marginTop: 2 }, sectionTitle: { fontSize: 16, fontWeight: '800', color: INK, letterSpacing: -0.25 }, link: { color: GREEN, fontSize: 11, fontWeight: '700' }, actionGrid: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 25 }, actionItem: { width: '23%', alignItems: 'center', gap: 8 }, iconTile: { width: 49, height: 49, borderRadius: 17, alignItems: 'center', justifyContent: 'center' }, actionLabel: { fontSize: 10, lineHeight: 14, color: '#35473A', textAlign: 'center', fontWeight: '700' },
  card: { backgroundColor: '#FFFFFF', borderRadius: 20, borderWidth: 1, borderColor: '#E9EDE6', padding: 14 }, statsRow: { flexDirection: 'row', gap: 9, marginBottom: 25 }, statCard: { flex: 1, padding: 11, borderRadius: 17 }, statNumber: { fontSize: 23, fontWeight: '800', color: INK, marginTop: 9 }, statLabel: { fontSize: 9, color: MUTED, marginTop: 1 }, taskRow: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingVertical: 11, borderBottomWidth: 1, borderBottomColor: '#F0F2ED' }, taskCheck: { width: 21, height: 21, borderRadius: 7, borderWidth: 1.5, borderColor: '#B8C8B7', alignItems: 'center', justifyContent: 'center' }, taskCheckDone: { backgroundColor: GREEN, borderColor: GREEN }, taskTitle: { fontSize: 12, fontWeight: '700', color: INK }, taskTime: { fontSize: 10, color: MUTED, marginTop: 4 }, taskDoneText: { textDecorationLine: 'line-through', color: MUTED },
  pageHeader: { marginTop: 10, marginBottom: 22 }, pageTitle: { fontSize: 27, fontWeight: '800', color: DEEP, letterSpacing: -0.8 }, pageSubtitle: { fontSize: 13, color: MUTED, marginTop: 6, lineHeight: 19 }, scanPreview: { height: 310, borderRadius: 25, backgroundColor: '#E5EFE1', overflow: 'hidden', alignItems: 'center', justifyContent: 'center', marginBottom: 14 }, selectedPhoto: { width: '100%', height: '100%' }, scanPlaceholder: { alignItems: 'center', gap: 10 }, scanPlaceholderTitle: { fontSize: 15, fontWeight: '800', color: DEEP }, scanPlaceholderText: { fontSize: 11, color: MUTED }, scanCorners: { ...StyleSheet.absoluteFillObject, margin: 25 }, cornerTL: { position: 'absolute', left: 0, top: 0, width: 34, height: 34, borderLeftWidth: 4, borderTopWidth: 4, borderColor: GREEN, borderTopLeftRadius: 12 }, cornerTR: { position: 'absolute', right: 0, top: 0, width: 34, height: 34, borderRightWidth: 4, borderTopWidth: 4, borderColor: GREEN, borderTopRightRadius: 12 }, cornerBL: { position: 'absolute', left: 0, bottom: 0, width: 34, height: 34, borderLeftWidth: 4, borderBottomWidth: 4, borderColor: GREEN, borderBottomLeftRadius: 12 }, cornerBR: { position: 'absolute', right: 0, bottom: 0, width: 34, height: 34, borderRightWidth: 4, borderBottomWidth: 4, borderColor: GREEN, borderBottomRightRadius: 12 },
  twoButtons: { flexDirection: 'row', gap: 10, marginBottom: 10 }, primaryButton: { flexDirection: 'row', gap: 8, alignItems: 'center', justifyContent: 'center', backgroundColor: GREEN, paddingVertical: 14, paddingHorizontal: 15, borderRadius: 15, flex: 1 }, primaryButtonText: { color: '#FFFFFF', fontSize: 12, fontWeight: '800' }, secondaryButton: { flexDirection: 'row', gap: 8, alignItems: 'center', justifyContent: 'center', backgroundColor: '#FFFFFF', borderWidth: 1, borderColor: '#D7E4D5', paddingVertical: 13, paddingHorizontal: 13, borderRadius: 15, flex: 1 }, secondaryButtonText: { color: GREEN, fontSize: 12, fontWeight: '800' }, fullButton: { flex: 0, marginBottom: 18 }, infoBox: { flexDirection: 'row', alignItems: 'flex-start', gap: 10, backgroundColor: '#EAF4E8', borderRadius: 15, padding: 13, marginBottom: 24 }, infoText: { flex: 1, fontSize: 11, color: '#46634B', lineHeight: 17 }, tipRow: { flexDirection: 'row', alignItems: 'center', gap: 11, marginBottom: 14 }, tipNumber: { width: 26, height: 26, borderRadius: 9, backgroundColor: '#E4F0E1', alignItems: 'center', justifyContent: 'center' }, tipNumberText: { color: GREEN, fontSize: 11, fontWeight: '800' }, tipText: { flex: 1, fontSize: 12, color: '#4E5D51', lineHeight: 18 },
  aiHero: { alignItems: 'center', backgroundColor: DEEP, borderRadius: 26, paddingHorizontal: 20, paddingTop: 22, paddingBottom: 18, marginBottom: 24 }, aiFarmer: { width: 112, height: 112, borderRadius: 56, borderWidth: 4, borderColor: '#75B987', marginBottom: 13 }, aiGreeting: { fontSize: 20, color: '#FFFFFF', fontWeight: '800' }, aiHint: { fontSize: 11, color: '#C6DFCA', marginTop: 7, textAlign: 'center' }, micButton: { width: 74, height: 74, borderRadius: 37, backgroundColor: '#2E9C5C', alignItems: 'center', justifyContent: 'center', marginTop: 20, borderWidth: 5, borderColor: '#387B50' }, micButtonActive: { backgroundColor: '#D36A4D', borderColor: '#9E503D' }, micCaption: { color: '#D6E9D8', fontSize: 10, marginTop: 8, fontWeight: '700' }, languageSelectWide: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: '#FFFFFF', borderRadius: 13, padding: 12, marginTop: 20, alignSelf: 'stretch' }, languageSelectText: { flex: 1, color: GREEN, fontSize: 11, fontWeight: '700' }, promptRow: { flexDirection: 'row', alignItems: 'center', gap: 11, backgroundColor: '#FFFFFF', padding: 13, borderRadius: 15, borderWidth: 1, borderColor: '#E7EDE4', marginBottom: 9 }, promptIcon: { width: 36, height: 36, borderRadius: 12, backgroundColor: MINT, alignItems: 'center', justifyContent: 'center' }, promptText: { flex: 1, color: INK, fontSize: 12, fontWeight: '600' },
  planBanner: { flexDirection: 'row', alignItems: 'center', backgroundColor: DEEP, borderRadius: 22, padding: 18, marginBottom: 25 }, planEyebrow: { color: '#A9D5B1', fontSize: 9, fontWeight: '800', letterSpacing: 1 }, planTitle: { color: '#FFFFFF', fontSize: 18, lineHeight: 23, fontWeight: '800', marginTop: 7, maxWidth: 230 }, planBody: { color: '#D3E8D5', fontSize: 11, lineHeight: 17, marginTop: 7, maxWidth: 230 }, plannerTask: { flexDirection: 'row', alignItems: 'center', gap: 11, paddingVertical: 14, borderBottomWidth: 1, borderBottomColor: '#EFF2EC' }, toolList: { backgroundColor: '#FFFFFF', borderRadius: 20, borderWidth: 1, borderColor: '#E9EDE6', paddingHorizontal: 13, marginBottom: 20 }, toolRow: { flexDirection: 'row', alignItems: 'center', gap: 12, paddingVertical: 13, borderBottomWidth: 1, borderBottomColor: '#F0F2ED' }, toolName: { flex: 1, color: INK, fontSize: 12, fontWeight: '700' }, toolSub: { color: MUTED, fontSize: 10, marginTop: 3 },
  profileCard: { alignItems: 'center', paddingVertical: 22, marginBottom: 25 }, profileAvatar: { width: 98, height: 98, borderRadius: 49, marginBottom: 12 }, profileName: { color: INK, fontWeight: '800', fontSize: 19 }, profileDetail: { color: MUTED, fontSize: 11, marginTop: 5, marginBottom: 16 }, version: { textAlign: 'center', color: '#9AA69A', fontSize: 10, marginVertical: 7 },
  tabBar: { flexDirection: 'row', backgroundColor: '#FFFFFF', borderTopWidth: 1, borderTopColor: '#E6EBE2', paddingTop: 8, paddingBottom: 8, paddingHorizontal: 5 }, tabItem: { flex: 1, alignItems: 'center', gap: 3 }, tabIconWrap: { width: 40, height: 30, borderRadius: 12, alignItems: 'center', justifyContent: 'center' }, tabIconActive: { backgroundColor: GREEN }, tabLabel: { fontSize: 9, color: MUTED, fontWeight: '600' }, tabLabelActive: { color: GREEN, fontWeight: '800' },
  locationBanner: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: '#EAF4E8', borderRadius: 17, padding: 13, marginBottom: 22 }, authSheet: { maxHeight: '92%', backgroundColor: BG, borderTopLeftRadius: 28, borderTopRightRadius: 28, paddingHorizontal: 23, paddingTop: 12, paddingBottom: 24 }, authSwitch: { flexDirection: 'row', backgroundColor: '#E8EEE5', padding: 4, borderRadius: 13, marginBottom: 16 }, authModeButton: { flex: 1, padding: 11, alignItems: 'center', borderRadius: 10 }, authModeActive: { backgroundColor: GREEN }, authModeText: { color: MUTED, fontWeight: '700' }, authModeTextActive: { color: '#FFFFFF' }, fieldLabel: { color: INK, fontSize: 11, fontWeight: '700', marginBottom: 6, marginTop: 8 }, textField: { backgroundColor: '#FFFFFF', borderWidth: 1, borderColor: '#DDE6D9', borderRadius: 12, paddingHorizontal: 13, paddingVertical: 12, color: INK, fontSize: 13 }, formSection: { color: DEEP, fontWeight: '800', fontSize: 15, marginTop: 18, marginBottom: 5 }, fieldRow: { flexDirection: 'row', gap: 10 },
  modalScrim: { flex: 1, justifyContent: 'flex-end', backgroundColor: 'rgba(12,31,18,0.4)' }, languageSheet: { backgroundColor: BG, borderTopLeftRadius: 28, borderTopRightRadius: 28, paddingHorizontal: 23, paddingTop: 12, paddingBottom: 30 }, sheetHandle: { width: 42, height: 4, borderRadius: 3, backgroundColor: '#CAD4C8', alignSelf: 'center', marginBottom: 18 }, sheetTitle: { fontSize: 22, fontWeight: '800', color: DEEP }, sheetSubtitle: { fontSize: 12, color: MUTED, marginTop: 5, marginBottom: 15 }, languageOption: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 13, borderBottomWidth: 1, borderBottomColor: '#E5EAE1' }, languageOptionText: { color: INK, fontSize: 14, fontWeight: '500' }, radioEmpty: { width: 19, height: 19, borderRadius: 10, borderWidth: 1.5, borderColor: '#C3CEC0' },
});
