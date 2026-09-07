import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ChatService } from './chat';

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

  it('envía el historial completo a POST /api/chat', async () => {
    const first = service.send('Hola');
    const firstRequest = httpMock.expectOne('/api/chat');
    expect(firstRequest.request.method).toBe('POST');
    expect(firstRequest.request.body).toEqual({
      messages: [{ role: 'user', content: 'Hola' }],
    });
    firstRequest.flush({ reply: '¡Hola!' });
    await first;

    const second = service.send('¿Cómo estás?');
    const secondRequest = httpMock.expectOne('/api/chat');
    expect(secondRequest.request.body).toEqual({
      messages: [
        { role: 'user', content: 'Hola' },
        { role: 'assistant', content: '¡Hola!' },
        { role: 'user', content: '¿Cómo estás?' },
      ],
    });
    secondRequest.flush({ reply: 'Muy bien, gracias' });
    await second;
  });

  it('agrega la respuesta al historial y limpia loading', async () => {
    const promise = service.send('Hola');
    expect(service.loading()).toBe(true);

    httpMock.expectOne('/api/chat').flush({ reply: 'Hola, ¿en qué te ayudo?' });
    await promise;

    expect(service.loading()).toBe(false);
    expect(service.error()).toBeNull();
    expect(service.messages()).toEqual([
      { role: 'user', content: 'Hola' },
      { role: 'assistant', content: 'Hola, ¿en qué te ayudo?' },
    ]);
  });

  it('en un error setea error con el detail y quita el mensaje fallido', async () => {
    const promise = service.send('Mensaje que va a fallar');
    httpMock
      .expectOne('/api/chat')
      .flush({ detail: 'Modelo no disponible' }, { status: 503, statusText: 'Service Unavailable' });
    await promise;

    expect(service.loading()).toBe(false);
    expect(service.error()).toBe('Modelo no disponible');
    expect(service.messages()).toEqual([]);
  });

  it('en un error sin detail usa un mensaje según el estado HTTP', async () => {
    const promise = service.send('Otro mensaje');
    httpMock.expectOne('/api/chat').flush(null, { status: 502, statusText: 'Bad Gateway' });
    await promise;

    expect(service.error()).toBe('El servidor respondió con un error. Inténtalo de nuevo.');
    expect(service.messages()).toEqual([]);
  });

  it('ignora envíos en blanco o mientras ya está cargando', () => {
    service.send('   ');
    expect(service.messages()).toEqual([]);
    expect(service.loading()).toBe(false);
  });
});