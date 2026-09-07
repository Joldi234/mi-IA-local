import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { ChatMessage } from '../models/message';

@Component({
  selector: 'app-message-list',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="message-list" aria-live="polite">
      @for (message of messages(); track $index) {
        <div class="chat-bubble" [class.user]="message.role === 'user'">
          <p>{{ message.content }}</p>
        </div>
      } @empty {
        <p class="chat-empty">Escribe tu primer mensaje para comenzar.</p>
      }
      @if (loading()) {
        <div class="chat-bubble assistant chat-typing">Escribiendo…</div>
      }
    </div>
  `,
})
export class MessageList {
  readonly messages = input<ChatMessage[]>([]);
  readonly loading = input(false);
}