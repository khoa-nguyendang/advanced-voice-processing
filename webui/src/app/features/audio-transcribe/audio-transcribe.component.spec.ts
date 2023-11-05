import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AudioTranscribeComponent } from './audio-transcribe.component';

describe('AudioTranscribeComponent', () => {
  let component: AudioTranscribeComponent;
  let fixture: ComponentFixture<AudioTranscribeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AudioTranscribeComponent]
    });
    fixture = TestBed.createComponent(AudioTranscribeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
