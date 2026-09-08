import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  TestRequest,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { ChatService } from './chat';
import { Conversation, StoredMessage } from '../models/conversation';

const anyConversationRequest = (req: { url: string }): boolean =>
  req.url.startsWith('/api/conversations');

const convA: Conversation = { id: 1, title: 'A', created_at: '', updated_at: '' };
const convB: Conversation = { id: 2, title: 'B', created_at: '', updated_at: '' };

const m1: StoredMessage = { id: 1, conversation_id: 1, role: 'user', content: 'Hola A', created_at: '' };
const m2: StoredMessage = { id: 2, conversation_id: 2, role: 'assistant', content: 'Respuesta B', created_at: '' };

async function waitForRequest(
  httpMock: HttpTestingController,
  url: string,
): Promise<TestRequest> {
  for (let i = 0; i < 50; i += 1) {
    const requests = httpMock.match(url);
    if (requests.length > 0) {
      return requests[0];
    }
    await new Promise((resolve) => setTimeout(resolve, 0));
  }
  throw new Error(`No request issued for ${url}`);
}

describe('ChatService', () => {
  let service: ChatService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(ChatService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('init con conversaciones selecciona la primera y carga su historial', async () => {
    const promise = service.init();
    httpMock.expectOne('/api/conversations').flush([convA, convB]);

    const messagesRequest = await waitForRequest(httpMock, '/api/conversations/1/messages');
    messagesRequest.flush([m1]);
    await promise;

    expect(service.selectedConversationId()).toBe(1);
    expect(service.messages()).toEqual([{ role: 'user', content: 'Hola A' }]);
    expect(service.conversations()).toEqual([convA, convB]);
    expect(service.loading()).toBe(false);
  });

  it('init sin conversaciones deja estado vacío', async () => {
    const promise = service.init();
    httpMock.expectOne('/api/conversations').flush([]);
    await promise;

    expect(service.selectedConversationId()).toBeNull();
    expect(service.messages()).toEqual([]);
    expect(service.loading()).toBe(false);
  });

  it('select cambia la conversación y reemplaza messages sin mezclar', async () => {
    service.conversations.set([convA, convB]);
    service.selectedConversationId.set(1);
    service.messages.set([{ role: 'user', content: 'Hola A' }]);

    const promise = service.select(2);
    httpMock.expectOne('/api/conversations/2/messages').flush([m2]);
    await promise;

    expect(service.selectedConversationId()).toBe(2);
    expect(service.messages()).toEqual([{ role: 'assistant', content: 'Respuesta B' }]);
  });

  it('create agrega la conversación al inicio, la selecciona y no emite GET messages', async () => {
    const promise = service.create();
    const req = httpMock.expectOne('/api/conversations');
    expect(req.request.method).toBe('POST');
    req.flush(convA);
    await promise;
    httpMock.expectNone(anyConversationRequest);

    expect(service.conversations()).toEqual([convA]);
    expect(service.selectedConversationId()).toBe(1);
    expect(service.messages()).toEqual([]);
  });

  it('send es optimista: muestra el user durante la llamada y el assistant al final', async () => {
    service.selectedConversationId.set(1);
    service.messages.set([]);

    const promise = service.send('Hola');
    expect(service.messages()).toEqual([{ role: 'user', content: 'Hola' }]);
    expect(service.loading()).toBe(true);

    httpMock.expectOne('/api/conversations/1/messages').flush({
      id: 5,
      conversation_id: 1,
      role: 'assistant',
      content: '¡Hola!',
      created_at: '',
    });
    await promise;

    expect(service.loading()).toBe(false);
    expect(service.messages()).toEqual([
      { role: 'user', content: 'Hola' },
      { role: 'assistant', content: '¡Hola!' },
    ]);
  });

  it('send reordena la conversación al tope tras la respuesta', async () => {
    service.conversations.set([convA, convB]);
    service.selectedConversationId.set(2);

    const promise = service.send('Hola');
    httpMock.expectOne('/api/conversations/2/messages').flush({
      id: 6,
      conversation_id: 2,
      role: 'assistant',
      content: 'Respuesta',
      created_at: '',
    });
    await promise;

    expect(service.conversations().map((c) => c.id)).toEqual([2, 1]);
  });

  it('ignora envíos en blanco o mientras ya está cargando', async () => {
    service.selectedConversationId.set(1);
    service.loading.set(true);
    await service.send('Hola');
    httpMock.expectNone(anyConversationRequest);

    service.loading.set(false);
    await service.send('   ');
    httpMock.expectNone(anyConversationRequest);
    expect(service.messages()).toEqual([]);
  });

  it('en error de send conserva el error y resincroniza con el backend', async () => {
    service.conversations.set([convA, convB]);
    service.selectedConversationId.set(1);
    service.messages.set([]);

    const promise = service.send('Hola');
    httpMock.expectOne('/api/conversations/1/messages').flush(
      { detail: 'Modelo no disponible' },
      { status: 503, statusText: 'Service Unavailable' },
    );

    const resyncRequest = await waitForRequest(httpMock, '/api/conversations/1/messages');
    expect(resyncRequest.request.method).toBe('GET');
    resyncRequest.flush([m1]);
    await promise;

    expect(service.error()).toBe('Modelo no disponible');
    expect(service.loading()).toBe(false);
    expect(service.messages()).toEqual([{ role: 'user', content: 'Hola A' }]);
  });

  it('si no hay conversación seleccionada, send setea un error y no hace HTTP', async () => {
    await service.send('Hola');
    expect(service.error()).toBe('Seleccioná una conversación.');
    httpMock.expectNone(anyConversationRequest);
  });

  it('404 en resync deja la conversación sin seleccionar y refresca la lista', async () => {
    service.conversations.set([convA, convB]);
    service.selectedConversationId.set(1);
    service.messages.set([{ role: 'user', content: 'Hola' }]);

    const promise = service.send('Hola');
    httpMock.expectOne('/api/conversations/1/messages').flush(
      { detail: 'Modelo no disponible' },
      { status: 503, statusText: 'Service Unavailable' },
    );

    const resyncRequest = await waitForRequest(httpMock, '/api/conversations/1/messages');
    resyncRequest.flush(
      { detail: 'La conversación no existe.' },
      { status: 404, statusText: 'Not Found' },
    );

    const listRequest = await waitForRequest(httpMock, '/api/conversations');
    expect(listRequest.request.method).toBe('GET');
    listRequest.flush([convB]);
    await promise;

    expect(service.selectedConversationId()).toBeNull();
    expect(service.conversations()).toEqual([convB]);
    expect(service.error()).toBe('Modelo no disponible');
  });

  it('404 en select mapea el error', async () => {
    const promise = service.select(99);
    httpMock.expectOne('/api/conversations/99/messages').flush(
      { detail: 'La conversación no existe.' },
      { status: 404, statusText: 'Not Found' },
    );
    await promise;

    expect(service.error()).toBe('La conversación no existe.');
    expect(service.loading()).toBe(false);
  });
});