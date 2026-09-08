import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ConversationService } from './conversation';

describe('ConversationService', () => {
  let service: ConversationService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(ConversationService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('list hace GET a /api/conversations', async () => {
    const promise = service.list();
    const req = httpMock.expectOne('/api/conversations');
    expect(req.request.method).toBe('GET');
    req.flush([{ id: 1, title: 'A', created_at: '', updated_at: '' }]);
    await expect(promise).resolves.toEqual([
      { id: 1, title: 'A', created_at: '', updated_at: '' },
    ]);
  });

  it('create hace POST a /api/conversations con body { title }', async () => {
    const promise = service.create('Mi título');
    const req = httpMock.expectOne('/api/conversations');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ title: 'Mi título' });
    req.flush({ id: 2, title: 'Mi título', created_at: '', updated_at: '' });
    await expect(promise).resolves.toEqual({
      id: 2,
      title: 'Mi título',
      created_at: '',
      updated_at: '',
    });
  });

  it('create sin título manda body {} para usar el title por defecto del backend', async () => {
    const promise = service.create();
    const req = httpMock.expectOne('/api/conversations');
    expect(req.request.body).toEqual({});
    expect(req.request.body?.title).toBeUndefined();
    req.flush({ id: 3, title: 'Nueva conversación', created_at: '', updated_at: '' });
    await expect(promise).resolves.toEqual({
      id: 3,
      title: 'Nueva conversación',
      created_at: '',
      updated_at: '',
    });
  });

  it('messages hace GET a /api/conversations/{id}/messages', async () => {
    const promise = service.messages(7);
    const req = httpMock.expectOne('/api/conversations/7/messages');
    expect(req.request.method).toBe('GET');
    req.flush([{ id: 10, conversation_id: 7, role: 'user', content: 'Hola', created_at: '' }]);
    await expect(promise).resolves.toEqual([
      { id: 10, conversation_id: 7, role: 'user', content: 'Hola', created_at: '' },
    ]);
  });

  it('sendMessage hace POST a /api/conversations/{id}/messages con body { content }', async () => {
    const promise = service.sendMessage(7, 'Hola');
    const req = httpMock.expectOne('/api/conversations/7/messages');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ content: 'Hola' });
    req.flush({
      id: 11,
      conversation_id: 7,
      role: 'assistant',
      content: '¡Hola!',
      created_at: '',
    });
    await expect(promise).resolves.toEqual({
      id: 11,
      conversation_id: 7,
      role: 'assistant',
      content: '¡Hola!',
      created_at: '',
    });
  });

  it('propaga errores HTTP sin mapearlos (404 y 503)', async () => {
    const notFound = service.messages(99);
    httpMock.expectOne('/api/conversations/99/messages').flush(
      { detail: 'No existe.' },
      { status: 404, statusText: 'Not Found' },
    );
    await expect(notFound).rejects.toMatchObject({ status: 404 });

    const unavailable = service.sendMessage(99, 'hola');
    httpMock
      .expectOne('/api/conversations/99/messages')
      .flush({ detail: 'Modelo no disponible' }, { status: 503, statusText: 'Service Unavailable' });
    await expect(unavailable).rejects.toMatchObject({ status: 503 });
  });
});
