import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PeopleutilisationComponent } from './peopleutilisation.component';

describe('PeopleutilisationComponent', () => {
  let component: PeopleutilisationComponent;
  let fixture: ComponentFixture<PeopleutilisationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PeopleutilisationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PeopleutilisationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
