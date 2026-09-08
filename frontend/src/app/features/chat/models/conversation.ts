import { ChatRole } from './message';

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface StoredMessage {
  id: number;
  conversation_id: number;
  role: ChatRole;
  content: string;
  created_at: string;
}
