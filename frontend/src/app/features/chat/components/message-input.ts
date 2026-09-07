import { ChangeDetectionStrategy, Component, input, output, signal } from '@angular/core';

@Component({
  selector: 'app-message-input',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <form class="chat-input" (submit)="submit($event)">
      <input
        #message
        type="text"
        [value]="text()"
        (input)="text.set(message.value)"
        [disabled]="disabled()"
        placeholder="Escribe un mensaje…"
        aria-label="Mensaje"
      />
      <button type="submit" [disabled]="disabled() || !text().trim()">Enviar</button>
    </form>
  `,
})
export class MessageInput {
  readonly disabled = input(false);
  readonly submitted = output<string>();

  protected readonly text = signal('');

  submit(event: SubmitEvent): void {
    event.preventDefault();
    const content = this.text().trim();
    if (!content || this.disabled()) {
      return;
    }
    this.text.set('');
    this.submitted.emit(content);
  }
}