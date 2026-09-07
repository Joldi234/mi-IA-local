export const CHAT_ROLE = {
  user: 'user',
  assistant: 'assistant',
} as const;

export type ChatRole = (typeof CHAT_ROLE)[keyof typeof CHAT_ROLE];

export interface ChatMessage {
  role: ChatRole;
  content: string;
}

export interface ChatResponse {
  reply: string;
}