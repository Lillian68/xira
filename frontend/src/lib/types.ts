export interface User {
  id: number;
  email: string;
  username: string;
}

export interface HerbSpirit {
  id: number;
  name: string;
  name_en: string;
  img_prefix: string;
  rarity: number;
  weight: number;
  germinate_time: number;
  grow_time: number;
  desc: string;
  desc_en: string;
}

export interface Resource {
  platform: string;
  title: string;
  url: string;
}

export interface Task {
  id: number;
  plan_id: number;
  day_number: number;
  title: string;
  content: string;
  resources: Resource[];
  knowledge_points: string[];
  is_completed: boolean;
  completed_at: string | null;
}

export interface Check {
  id: number;
  plan_id: number;
  day_number: number;
  questions_json: string;
  result_json: string;
  passed: boolean;
  created_at?: string;
}

export interface Result {
  id: number;
  plan_id: number;
  actual_result: string;
  diagnosis: string;
  diagnosis_detail: string;
  remedy_plan_json: string;
  created_at?: string;
}

export interface StudyPlan {
  id: number;
  user_id: number;
  workflow_id: string;
  target: string;
  target_type: string;
  current_stage: string;
  daily_study_time: number;
  start_date: string;
  end_date: string;
  check_interval: number;
  created_at?: string;
  spirit?: HerbSpirit | null;
  status: string;
  tasks?: Task[];
  checks?: Check[];
  result?: Result;
  task_id: string;
}
