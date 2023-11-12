import { AsyncPipe, CommonModule, NgClass, NgForOf } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from "@angular/core";
import { FormsModule } from "@angular/forms";
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
        CommonModule,
        FormsModule
    ],
    standalone: true,
})
export class HomeComponent implements OnInit, OnDestroy {
    fileName = '';
    audioContext;
    textInput = '';
    errorMessage = '';
    processing = false;
    @ViewChild('audioResult') audioResult: ElementRef<HTMLAudioElement> | undefined;

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

    onSubmit(event: any) {
        event.preventDefault();

        this.processing = true;
        let body = JSON.stringify({ text : this.textInput});
        const upload$ = this.http.post("/text-to-speech", body , {
            headers: {'Content-Type': 'application/json'},
            responseType: 'blob'
        });

        upload$.subscribe({
            next: (res: any) => { this.playBlob(res); },
            error: (error: any) => {
                console.log(error)
                this.errorMessage = error;
                this.processing = false;
            },
            complete: () => { this.processing = false; }
        });
    }

    onErrorReceivingBuffer(err: any) {
        this.errorMessage = err;
    }

    playBlob(blob: Blob) {
        let el = this.audioResult?.nativeElement as HTMLAudioElement;
        el.src = URL.createObjectURL(blob);
        el.load();
        el.play();
    }

}
