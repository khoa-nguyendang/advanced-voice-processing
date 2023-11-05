import { AsyncPipe, NgClass, NgForOf } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { Component, OnDestroy, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { UserService } from "../../core/services/user.service";
import { ArticleListComponent } from "../../shared/article-helpers/article-list.component";
import { ShowAuthedDirective } from "../../shared/show-authed.directive";

@Component({
  selector: "app-home-page",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.css"],
  imports: [
    NgClass,
    ArticleListComponent,
    AsyncPipe,
    NgForOf,
    ShowAuthedDirective,
  ],
  standalone: true,
})
export class HomeComponent implements OnInit, OnDestroy {
    fileName = '';
    audioContext;
    text_result = '';
  constructor(
    private readonly router: Router,
    private readonly userService: UserService,
    private http: HttpClient
  ) {

    let AudioContext_ = AudioContext;
    this.audioContext = new AudioContext_();
  }

  ngOnInit(): void {
    
  }

  ngOnDestroy(): void {
  }

  onFileSelected(event: any) {

    const file:File = event.target.files[0];

    if (file) {

        this.fileName = file.name;

        const formData = new FormData();

        formData.append("file", file);
        formData.append("speaker", "khoaspeech");

        const upload$ = this.http.post("/text-to-speech", formData);

      
        upload$.subscribe();
    }
}

play(arrBf: any) {
    this.audioContext.decodeAudioData(arrBf, (buffer) => {
     let source = this.audioContext.createBufferSource(); 
     source.buffer = buffer;                   
     source.connect(this.audioContext.destination);       
     source.start(0);                          
    });
 }

}
