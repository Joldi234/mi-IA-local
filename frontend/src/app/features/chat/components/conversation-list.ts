import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { Conversation } from '../models/conversation';

@Component({
  selector: 'app-conversation-list',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="conversation-list">
      <button
        class="btn-new"
        type="button"
        [disabled]="disabled()"
        (click)="createNew.emit()"
      >
        Nueva conversación
      </button>
      @for (conversation of conversations(); track conversation.id) {
        <button
          class="conversation-item"
          type="button"
          [class.selected]="conversation.id === selectedId()"
          [disabled]="disabled()"
          [attr.aria-current]="conversation.id === selectedId() ? 'true' : null"
          (click)="selectChange.emit(conversation.id)"
        >
          <span class="conversation-title">{{ conversation.title }}</span>
          <span class="conversation-date">{{ formatDate(conversation.updated_at) }}</span>
        </button>
      } @empty {
        @if (!conversations().length) {
          <p class="conversation-empty">No hay conversaciones. Creá la primera.</p>
        }
      }
    </div>
  `,
})
export class ConversationList {
  readonly conversations = input<Conversation[]>([]);
  readonly selectedId = input<number | null>(null);
  readonly disabled = input(false);

  readonly selectChange = output<number>();
  readonly createNew = output<void>();

  formatDate(value: string): string {
    return new Date(value).toLocaleString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  }
}
