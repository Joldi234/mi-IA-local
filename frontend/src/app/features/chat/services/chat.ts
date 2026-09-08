import { Injectable, inject, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ChatMessage } from '../models/message';
import { Conversation, StoredMessage } from '../models/conversation';
import { ConversationService } from './conversation';

function toChatMessage(message: StoredMessage): ChatMessage {
  return { role: message.role, content: message.content };
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  private readonly conversationService = inject(ConversationService);

  readonly conversations = signal<Conversation[]>([]);
  readonly selectedConversationId = signal<number | null>(null);
  readonly messages = signal<ChatMessage[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  async init(): Promise<void> {
    this.loading.set(true);
    try {
      const conversations = await this.conversationService.list();
      this.conversations.set(conversations);
      if (conversations.length > 0) {
        await this.select(conversations[0].id);
      }
    } catch (error) {
      this.error.set(this.errorMessage(error));
    } finally {
      this.loading.set(false);
    }
  }

  async select(id: number): Promise<void> {
    this.selectedConversationId.set(id);
    this.loading.set(true);
    try {
      const stored = await this.conversationService.messages(id);
      this.messages.set(stored.map(toChatMessage));
    } catch (error) {
      this.error.set(this.errorMessage(error));
    } finally {
      this.loading.set(false);
    }
  }

  async create(): Promise<void> {
    this.loading.set(true);
    try {
      const conversation = await this.conversationService.create();
      this.conversations.update((current) => [conversation, ...current]);
      this.selectedConversationId.set(conversation.id);
      this.messages.set([]);
    } catch (error) {
      this.error.set(this.errorMessage(error));
    } finally {
      this.loading.set(false);
    }
  }

  async send(content: string): Promise<void> {
    const text = content.trim();
    if (!text || this.loading()) {
      return;
    }
    const id = this.selectedConversationId();
    if (id === null) {
      this.error.set('Seleccioná una conversación.');
      return;
    }

    const userMessage: ChatMessage = { role: 'user', content: text };
    this.messages.update((current) => [...current, userMessage]);
    this.loading.set(true);
    this.error.set(null);

    try {
      const assistant = await this.conversationService.sendMessage(id, text);
      this.messages.update((current) => [
        ...current,
        { role: 'assistant', content: assistant.content },
      ]);
      this.conversations.update((current) => {
        const conversation = current.find((c) => c.id === id);
        return conversation ? [conversation, ...current.filter((c) => c.id !== id)] : current;
      });
    } catch (error) {
      this.error.set(this.errorMessage(error));
      try {
        const real = await this.conversationService.messages(id);
        this.messages.set(real.map(toChatMessage));
      } catch (syncError) {
        if (syncError instanceof HttpErrorResponse && syncError.status === 404) {
          this.selectedConversationId.set(null);
          try {
            this.conversations.set(await this.conversationService.list());
          } catch {
            // conserva el error original de send
          }
        }
      }
    } finally {
      this.loading.set(false);
    }
  }

  private errorMessage(error: unknown): string {
    if (error instanceof HttpErrorResponse) {
      const detail = (error.error as { detail?: unknown } | null)?.detail;
      if (typeof detail === 'string' && detail) {
        return detail;
      }
      return this.statusMessage(error.status);
    }
    return 'No se pudo conectar con el servidor. Inténtalo de nuevo.';
  }

  private statusMessage(status: number): string {
    switch (status) {
      case 503:
        return 'El modelo no está disponible en este momento. Inténtalo de nuevo en unos segundos.';
      case 404:
        return 'No se encontró el servicio de chat.';
      case 504:
        return 'El servidor tardó demasiado en responder. Inténtalo de nuevo.';
      case 502:
        return 'El servidor respondió con un error. Inténtalo de nuevo.';
      case 422:
        return 'La solicitud no pudo ser procesada.';
      default:
        return `Ocurrió un error inesperado (${status}). Inténtalo de nuevo.`;
    }
  }
}
