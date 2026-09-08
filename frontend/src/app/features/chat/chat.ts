import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { ConversationList } from './components/conversation-list';
import { MessageInput } from './components/message-input';
import { MessageList } from './components/message-list';
import { ChatService } from './services/chat';

@Component({
  selector: 'app-chat',
  imports: [ConversationList, MessageInput, MessageList],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="chat-layout">
      <aside class="conversation-sidebar">
        <app-conversation-list
          [conversations]="service.conversations()"
          [selectedId]="service.selectedConversationId()"
          [disabled]="service.loading()"
          (selectChange)="service.select($event)"
          (createNew)="service.create()"
        />
      </aside>
      <main class="chat">
        <header class="chat-header">
          <h2>{{ activeTitle() }}</h2>
        </header>
        <app-message-list [messages]="service.messages()" [loading]="service.loading()" />
        @if (service.error(); as error) {
          <div class="chat-error" role="alert">{{ error }}</div>
        }
        <app-message-input [disabled]="service.loading()" (submitted)="send($event)" />
      </main>
    </div>
  `,
})
export class Chat {
  protected readonly service = inject(ChatService);

  protected readonly activeTitle = computed(() => {
    const id = this.service.selectedConversationId();
    if (id === null) {
      return 'Nueva conversación';
    }
    const conversation = this.service.conversations().find((c) => c.id === id);
    return conversation?.title ?? 'Nueva conversación';
  });

  constructor() {
    void this.service.init();
  }

  send(content: string): void {
    void this.service.send(content);
  }
}
