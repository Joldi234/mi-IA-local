import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { MessageInput } from './components/message-input';
import { MessageList } from './components/message-list';
import { ChatService } from './services/chat';

@Component({
  selector: 'app-chat',
  imports: [MessageInput, MessageList],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <main class="chat">
      <app-message-list [messages]="service.messages()" [loading]="service.loading()" />
      @if (service.error(); as error) {
        <div class="chat-error" role="alert">{{ error }}</div>
      }
      <app-message-input [disabled]="service.loading()" (submitted)="send($event)" />
    </main>
  `,
})
export class Chat {
  protected readonly service = inject(ChatService);

  send(content: string): void {
    void this.service.send(content);
  }
}