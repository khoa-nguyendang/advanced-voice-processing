import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AudioTranslateComponent } from './audio-translate.component';

describe('AudioTranslateComponent', () => {
  let component: AudioTranslateComponent;
  let fixture: ComponentFixture<AudioTranslateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AudioTranslateComponent]
    });
    fixture = TestBed.createComponent(AudioTranslateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
