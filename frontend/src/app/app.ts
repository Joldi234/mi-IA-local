import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Chat } from './features/chat/chat';

@Component({
  selector: 'app-root',
  imports: [Chat],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <header class="app-header">
      <h1>mi-IA-local</h1>
      <p>Asistente local</p>
    </header>
    <app-chat />
  `,
})
export class App {}