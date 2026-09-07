import { ComponentFixture } from '@angular/core/testing';
import { TestBed } from '@angular/core/testing';
import { ChatMessage } from '../models/message';
import { MessageList } from './message-list';

function createList(messages: ChatMessage[], loading = false): ComponentFixture<MessageList> {
  const fixture = TestBed.createComponent(MessageList);
  fixture.componentRef.setInput('messages', messages);
  fixture.componentRef.setInput('loading', loading);
  fixture.detectChanges();
  return fixture;
}

describe('MessageList', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({ imports: [MessageList] });
  });

  it('muestra los mensajes que recibe por input', () => {
    const fixture = createList([
      { role: 'user', content: 'Hola' },
      { role: 'assistant', content: '¡Hola!' },
    ]);
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Hola');
    expect(text).toContain('¡Hola!');
  });

  it('muestra el indicador mientras loading es true', () => {
    const fixture = createList([], true);
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Escribiendo');
  });

  it('muestra el indicador junto a mensajes existentes', () => {
    const fixture = createList([{ role: 'user', content: 'Hola' }], true);
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Hola');
    expect(text).toContain('Escribiendo');
  });

  it('no muestra el indicador ni el estado vacío cuando hay mensajes y no carga', () => {
    const fixture = createList([{ role: 'assistant', content: 'Respuesta' }], false);
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Respuesta');
    expect(text).not.toContain('Escribiendo');
    expect(text).not.toContain('primer mensaje');
  });

  it('muestra el mensaje de bienvenida cuando no hay mensajes', () => {
    const fixture = createList([], false);
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Escribe tu primer mensaje');
  });
});