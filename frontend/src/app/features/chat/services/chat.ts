import { Injectable, inject, signal } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { ChatMessage, ChatResponse } from '../models/message';

@Injectable({ providedIn: 'root' })
export class ChatService {
  private readonly http = inject(HttpClient);

  readonly messages = signal<ChatMessage[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  async send(content: string): Promise<void> {
    const text = content.trim();
    if (!text || this.loading()) {
      return;
    }

    const userMessage: ChatMessage = { role: 'user', content: text };
    const history = [...this.messages(), userMessage];

    this.messages.set(history);
    this.loading.set(true);
    this.error.set(null);

    try {
      const response = await firstValueFrom(
        this.http.post<ChatResponse>('/api/chat', { messages: history }),
      );
      this.messages.update((current) => [
        ...current,
        { role: 'assistant', content: response.reply },
      ]);
    } catch (error) {
      this.messages.update((current) => current.filter((message) => message !== userMessage));
      this.error.set(this.errorMessage(error));
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