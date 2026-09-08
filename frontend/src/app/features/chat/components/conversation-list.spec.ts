import { ComponentFixture } from '@angular/core/testing';
import { TestBed } from '@angular/core/testing';
import { Conversation } from '../models/conversation';
import { ConversationList } from './conversation-list';

function createList(conversations: Conversation[], selectedId: number | null = null, disabled = false): ComponentFixture<ConversationList> {
  const fixture = TestBed.createComponent(ConversationList);
  fixture.componentRef.setInput('conversations', conversations);
  fixture.componentRef.setInput('selectedId', selectedId);
  fixture.componentRef.setInput('disabled', disabled);
  fixture.detectChanges();
  return fixture;
}

function elements(fixture: ComponentFixture<ConversationList>): {
  items: HTMLButtonElement[];
  newButton: HTMLButtonElement;
} {
  const el = fixture.nativeElement as HTMLElement;
  const items = Array.from(el.querySelectorAll('.conversation-item')) as HTMLButtonElement[];
  const newButton = el.querySelector('.btn-new') as HTMLButtonElement;
  return { items, newButton };
}

describe('ConversationList', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({ imports: [ConversationList] });
  });

  const conversations: Conversation[] = [
    { id: 1, title: 'Primera', created_at: '2026-01-01T10:00:00', updated_at: '2026-01-01T10:00:00' },
    { id: 2, title: 'Segunda', created_at: '2026-01-02T12:30:00', updated_at: '2026-01-02T12:30:00' },
  ];

  it('muestra título y fecha de cada conversación', () => {
    const fixture = createList(conversations);
    const { items } = elements(fixture);
    expect(items.length).toBe(2);
    expect(items[0].textContent).toContain('Primera');
    expect(items[0].textContent).toContain('10:00');
  });

  it('aplica la clase selected a la conversación activa', () => {
    const fixture = createList(conversations, 2);
    const { items } = elements(fixture);
    expect(items[1].classList.contains('selected')).toBe(true);
    expect(items[0].classList.contains('selected')).toBe(false);
    expect(items[1].getAttribute('aria-current')).toBe('true');
  });

  it('emite selectChange con el id al hacer click', () => {
    const fixture = createList(conversations);
    let emitted: number | undefined;
    fixture.componentInstance.selectChange.subscribe((id) => (emitted = id));
    const { items } = elements(fixture);
    items[1].click();
    expect(emitted).toBe(2);
  });

  it('emite createNew al hacer click en Nueva conversación', () => {
    const fixture = createList(conversations);
    let emitted = false;
    fixture.componentInstance.createNew.subscribe(() => (emitted = true));
    const { newButton } = elements(fixture);
    newButton.click();
    expect(emitted).toBe(true);
  });

  it('muestra el estado vacío sin conversaciones', () => {
    const fixture = createList([]);
    expect((fixture.nativeElement as HTMLElement).textContent).toContain(
      'No hay conversaciones. Creá la primera.',
    );
  });

  it('estando disabled no emite al hacer click', () => {
    const fixture = createList(conversations, null, true);
    let emitted = false;
    fixture.componentInstance.selectChange.subscribe(() => (emitted = true));
    const { items, newButton } = elements(fixture);
    items[0].click();
    newButton.click();
    expect(emitted).toBe(false);
    expect(newButton.disabled).toBe(true);
  });
});
