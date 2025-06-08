import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleHubComponent } from './article-hub.component';

describe('ArticleHubComponent', () => {
  let component: ArticleHubComponent;
  let fixture: ComponentFixture<ArticleHubComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ArticleHubComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ArticleHubComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
