import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssignmentrowComponent } from './assignmentrow.component';

describe('AssignmentrowComponent', () => {
  let component: AssignmentrowComponent;
  let fixture: ComponentFixture<AssignmentrowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AssignmentrowComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AssignmentrowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
