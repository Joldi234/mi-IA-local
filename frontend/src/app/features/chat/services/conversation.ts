import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { Conversation, StoredMessage } from '../models/conversation';

@Injectable({ providedIn: 'root' })
export class ConversationService {
  private readonly http = inject(HttpClient);

  list(): Promise<Conversation[]> {
    return firstValueFrom(this.http.get<Conversation[]>('/api/conversations'));
  }

  create(title?: string): Promise<Conversation> {
    // El backend requiere un body objeto (ConversationCreate); `{}` usa el title por defecto.
    const body = title ? { title } : {};
    return firstValueFrom(this.http.post<Conversation>('/api/conversations', body));
  }

  messages(id: number): Promise<StoredMessage[]> {
    return firstValueFrom(this.http.get<StoredMessage[]>(`/api/conversations/${id}/messages`));
  }

  sendMessage(id: number, content: string): Promise<StoredMessage> {
    return firstValueFrom(
      this.http.post<StoredMessage>(`/api/conversations/${id}/messages`, { content }),
    );
  }
}
