export const locales = ["zh", "en"] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = "zh";

export const translations: Record<Locale, {
  brand: string;
  headline: string;
  tagline: string;
  description: string;
  primaryCta: string;
  secondaryCta: string;
  about: string;
  close: string;
  xirang: string;
  appMeaning: string;
  login: string;
  register: string;
  emailOrUsername: string;
  email: string;
  username: string;
  password: string;
  noAccount: string;
  hasAccount: string;
  loading: string;
  loginFailed: string;
  registerFailed: string;
  logout: string;
  dashboardLoading: string;
  createTitle: string;
  createSubtitle: string;
  targetLabel: string;
  targetPlaceholder: string;
  targetTypeLabel: string;
  targetTypeExam: string;
  targetTypePractice: string;
  currentStageLabel: string;
  currentStagePlaceholder: string;
  dailyMinutesLabel: string;
  startDateLabel: string;
  endDateLabel: string;
  checkIntervalLabel: string;
  checkIntervalHint: string;
  nextStep: string;
  previousStep: string;
  generatePlan: string;
  generating: string;
  loadingSpirit: string;
  confirmSpirit: string;
  targetRequired: string;
  currentStageRequired: string;
  dailyMinutesRequired: string;
  totalDaysTooLong: string;
  dateRequired: string;
  startDatePast: string;
  endDateBeforeStart: string;
  checkIntervalRequired: string;
  loginRequired: string;
  taskIdMissing: string;
  submitFailed: string;
  spiritListening: string;
  spiritBreathing: string;
  you: string;
  spiritNoReply: string;
  spiritUnavailable: string;
  chatPlaceholder: string;
  createStepObservation: string;
  createStepListening: string;
  createStepInquiry: string;
  createStepDiagnosis: string;
  studyLoading: string;
  spiritLabel: string;
  dayShort: string;
  stageCheck: string;
  finalFeedback: string;
  completed: string;
  completeCheckin: string;
  checkinInProgress: string;
  stageCheckAfterDay: string;
  selfFeedback: string;
  selfFeedbackPlaceholder: string;
  submitFeedback: string;
  submittingFeedback: string;
  passed: string;
  needsStrengthening: string;
  noEvaluation: string;
  generatingChecklist: string;
  checklistPlaceholder: string;
  fetchStageCheckFailed: string;
  stageCheckTitle: string;
  stageCheckLoading: string;
  planAdjustmentFailed: string;
  loadingDiagnosis: string;
  diagnosisDetail: string;
  noDiagnosis: string;
  remedialPrompt: string;
  remedialPlaceholder: string;
  submitResult: string;
  submittingResult: string;
  spiritCheckinCelebration: string;
}> = {
  zh: {
    brand: "息壤",
    headline: "知你进取，",
    tagline: "共此生息。",
    description: "息壤，更懂你节奏的情感陪伴型自学引擎。",
    primaryCta: "开启自学之旅",
    secondaryCta: "了解更多",
    about: "关于息壤",
    close: "关闭",
    xirang: "在中国神话《山海经》中，息壤是能自生长、永不耗减的神土。知识的积淀像息壤一样，只要你不断投入，它就会自动生长，最终筑起你的精神堡垒。",
    appMeaning: "作为一款AI驱动的情感陪伴型自学引擎，用户通过与“中草药精灵”共同成长，将自学任务可视化为植物培育过程。知识如药。现代人的焦虑、迷茫是一种“病”，自学是自我疗愈的过程。你若勤奋，药草便灵气逼人，能医治你的焦虑；你若懒散，药草便枯萎，无法为你提供精神慰藉。",
    login: "登录",
    register: "注册",
    emailOrUsername: "邮箱或用户名",
    email: "邮箱",
    username: "用户名",
    password: "密码",
    noAccount: "尚无账号？",
    hasAccount: "已有账号？",
    loading: "加载中…",
    loginFailed: "登录失败",
    registerFailed: "注册失败",
    logout: "离开息壤",
    dashboardLoading: "大雾未散，息壤加载中…",
    createTitle: "四诊定制",
    createSubtitle: "望闻问切 — 一键生成学习计划",
    targetLabel: "学习目标",
    targetPlaceholder: "例：雅思8分 / 学会自由泳 / 掌握Python数据分析",
    targetTypeLabel: "目标类型",
    targetTypeExam: "考试",
    targetTypePractice: "实操",
    currentStageLabel: "当前现状",
    currentStagePlaceholder: "简单描述你目前掌握的水平、薄弱环节等情况",
    dailyMinutesLabel: "每日学习时长（分钟）",
    startDateLabel: "起始日期",
    endDateLabel: "结束日期",
    checkIntervalLabel: "阶段检验频率（天）",
    checkIntervalHint: "每隔N天复盘检验学习效果",
    nextStep: "下一步",
    previousStep: "上一步",
    generatePlan: "生成学习计划",
    generating: "生成中…",
    loadingSpirit: "加载精灵中…",
    confirmSpirit: "收下精灵，前往学习",
    targetRequired: "请填写学习目标",
    currentStageRequired: "请描述当前现状",
    dailyMinutesRequired: "每日学习时长需在 15～120 分钟之间",
    totalDaysTooLong: "学习总天数不能超过 7 天，请调整日期范围",
    dateRequired: "请选择起始日期和结束日期",
    startDatePast: "起始日期不能选择过去的日期",
    endDateBeforeStart: "结束日期不能早于起始日期",
    checkIntervalRequired: "阶段检验频率至少为1天",
    loginRequired: "请先登录",
    taskIdMissing: "未获取到任务ID，无法监听生成进度",
    submitFailed: "提交失败，请重试",
    spiritListening: "息壤微风，精灵正倾听……",
    spiritBreathing: "吐纳之间……",
    you: "你",
    spiritNoReply: "精灵暂无回应。",
    spiritUnavailable: "雾气稍重，暂时无法交流。",
    chatPlaceholder: "输入消息与精灵对话……",
    createStepObservation: "望",
    createStepListening: "闻",
    createStepInquiry: "问",
    createStepDiagnosis: "切",
    studyLoading: "加载中…",
    spiritLabel: "精灵",
    dayShort: "第",
    stageCheck: "阶段检验",
    finalFeedback: "终极反馈",
    completed: "已打卡",
    completeCheckin: "完成打卡",
    checkinInProgress: "浇灌中…",
    stageCheckAfterDay: "阶段检验（第 {day} 天后）",
    selfFeedback: "请输入你的自我反馈",
    selfFeedbackPlaceholder: "在此填写你的自我反馈……",
    submitFeedback: "提交反馈",
    submittingFeedback: "提交中…",
    passed: "检验通过",
    needsStrengthening: "尚需补强",
    noEvaluation: "暂无详细评价。",
    generatingChecklist: "正在生成自检清单…",
    checklistPlaceholder: "请输入你的自我反馈",
    fetchStageCheckFailed: "获取阶段检验失败",
    stageCheckTitle: "阶段检验",
    stageCheckLoading: "正在生成自检清单…",
    planAdjustmentFailed: "计划调整失败，请稍后手动更新",
    loadingDiagnosis: "正在加载已有诊断…",
    diagnosisDetail: "诊断详情",
    noDiagnosis: "暂无诊断内容",
    remedialPrompt: "申报真实结果，精灵开出后期补强方剂。",
    remedialPlaceholder: "例：雅思总分 6.5 / 项目未能跑通登录模块",
    submitResult: "提交反馈",
    submittingResult: "提交中…",
    spiritCheckinCelebration: "今日耕耘已记录，精灵为你鼓掌。",
  },
  en: {
    brand: "Xira",
    headline: "Your growth, nurtured.",
    tagline: "Never study alone.",
    description: "Let Xira be the companion who truly understands your pace.",
    primaryCta: "Start journey",
    secondaryCta: "Learn more",
    about: "About Xira",
    close: "Close",
    xirang: "In the ancient Chinese mythological work The Classic of Mountains and Seas, Xirang is divine soil capable of regenerating endlessly without depletion. The accumulation of knowledge is akin to Xirang: consistent investment of effort allows it to grow perpetually, eventually building a fortress for your inner spirit.",
    appMeaning: "This AI-powered emotional companion self-study engine lets users grow alongside 'Chinese Herbal Spirit Elves', visualizing self-learning tasks as the process of nurturing plants. Knowledge is herbal medicine. Modern anxiety and confusion are ailments, and self-study serves as a journey of self-healing. If you stay diligent, your herbal spirits will brim with vital aura, curing your inner restlessness. If you grow idle, the herbs will wither, unable to offer spiritual solace.",
    login: "Log in",
    register: "Register",
    emailOrUsername: "Email or username",
    email: "Email",
    username: "Username",
    password: "Password",
    noAccount: "No account yet?",
    hasAccount: "Already have an account?",
    loading: "Loading…",
    loginFailed: "Login failed",
    registerFailed: "Registration failed",
    logout: "Leave Xira",
    dashboardLoading: "The mist is still rising, Xira is loading…",
    createTitle: "Four Diagnostic Customization",
    createSubtitle: "Observe · Listen · Inquire · Diagnose — generate a study plan in one click",
    targetLabel: "Study goal",
    targetPlaceholder: "Example: IELTS 8.0 / learn freestyle swimming / master Python data analysis",
    targetTypeLabel: "Goal type",
    targetTypeExam: "Exam",
    targetTypePractice: "Practice",
    currentStageLabel: "Current situation",
    currentStagePlaceholder: "Briefly describe your current level, weak points, and any challenges",
    dailyMinutesLabel: "Daily study time (minutes)",
    startDateLabel: "Start date",
    endDateLabel: "End date",
    checkIntervalLabel: "Review frequency (days)",
    checkIntervalHint: "Review progress every N days",
    nextStep: "Next",
    previousStep: "Back",
    generatePlan: "Generate study plan",
    generating: "Generating…",
    loadingSpirit: "Loading spirit…",
    confirmSpirit: "Accept spirit and continue learning",
    targetRequired: "Please fill in your study goal",
    currentStageRequired: "Please describe your current situation",
    dailyMinutesRequired: "Daily study time must be between 15 and 120 minutes",
    totalDaysTooLong: "Total study days cannot exceed 7 days, please adjust date range",
    dateRequired: "Please select both start and end dates",
    startDatePast: "Start date cannot be in the past",
    endDateBeforeStart: "End date cannot be earlier than start date",
    checkIntervalRequired: "Review frequency must be at least 1 day",
    loginRequired: "Please log in first",
    taskIdMissing: "Task ID not received, cannot monitor generation progress",
    submitFailed: "Submission failed, please try again",
    spiritListening: "A breeze of Xirang stirs as the spirit listens…",
    spiritBreathing: "In the breath between moments…",
    you: "You",
    spiritNoReply: "The spirit has no reply for now.",
    spiritUnavailable: "The mist thickens; communication is temporarily unavailable.",
    chatPlaceholder: "Speak with spirit…",
    createStepObservation: "Observe",
    createStepListening: "Listen",
    createStepInquiry: "Inquire",
    createStepDiagnosis: "Diagnose",
    studyLoading: "Loading…",
    spiritLabel: "Spirit",
    dayShort: "Day",
    stageCheck: "Stage Check",
    finalFeedback: "Final Feedback",
    completed: "Completed",
    completeCheckin: "Complete check-in",
    checkinInProgress: "Watering…",
    stageCheckAfterDay: "Stage check (after day {day})",
    selfFeedback: "Please enter your self-assessment",
    selfFeedbackPlaceholder: "Write your self-assessment here…",
    submitFeedback: "Submit feedback",
    submittingFeedback: "Submitting…",
    passed: "Check passed",
    needsStrengthening: "Needs strengthening",
    noEvaluation: "No detailed evaluation yet.",
    generatingChecklist: "Generating self-check list…",
    checklistPlaceholder: "Please enter your self-assessment",
    fetchStageCheckFailed: "Failed to fetch stage check",
    stageCheckTitle: "Stage check",
    stageCheckLoading: "Generating self-check list…",
    planAdjustmentFailed: "Plan adjustment failed, please update manually later",
    loadingDiagnosis: "Loading diagnosis…",
    diagnosisDetail: "Diagnosis details",
    noDiagnosis: "No diagnosis content yet",
    remedialPrompt: "Report the real result and the spirit will prescribe a later strengthening recipe.",
    remedialPlaceholder: "Example: IELTS total 6.5 / project failed to complete the login flow",
    submitResult: "Submit feedback",
    submittingResult: "Submitting…",
    spiritCheckinCelebration: "Today's work is recorded. The spirit applauds you.",
  },
};

export function getLocaleFromBrowser(): Locale {
  if (typeof navigator === "undefined") {
    return defaultLocale;
  }

  const language = navigator.language.toLowerCase();
  if (language.startsWith("zh")) {
    return "zh";
  }

  return "en";
}
