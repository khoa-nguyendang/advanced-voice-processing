import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VoiceCloningComponent } from './voice-cloning.component';

describe('VoiceCloningComponent', () => {
  let component: VoiceCloningComponent;
  let fixture: ComponentFixture<VoiceCloningComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [VoiceCloningComponent]
    });
    fixture = TestBed.createComponent(VoiceCloningComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
