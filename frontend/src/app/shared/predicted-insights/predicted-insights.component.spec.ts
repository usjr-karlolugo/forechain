import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictedInsightsComponent } from './predicted-insights.component';

describe('PredictedInsightsComponent', () => {
  let component: PredictedInsightsComponent;
  let fixture: ComponentFixture<PredictedInsightsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PredictedInsightsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PredictedInsightsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
