import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SentimentFilterComponent } from './sentiment-filter.component';

describe('SentimentFilterComponent', () => {
  let component: SentimentFilterComponent;
  let fixture: ComponentFixture<SentimentFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SentimentFilterComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SentimentFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
