import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { BaseService } from './services/base.service';
import { HttpClientModule } from '@angular/common/http';
import { KeywordAnalysisService } from './services/keywordAnalysis.service';
import { MultiTranslateService } from './services/multiTranslate.service';
import { SubTitleSubctractService } from './services/subTitleSubctract.servise';
import { ClippingService } from './services/clipping.service';
import { response } from 'express';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, FormsModule, HttpClientModule],
  providers: [BaseService],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'Hangi Dakika';
  public customUrl: string;
  public isPlay: boolean = false;
  public pathUrl = "";
  public keyword;
  public myTimeout;
  public selectedLang;
  public _multiTranslate;
  public _translateLoop;
  public _subTopics;
  public _keywordAnalysis;
  public detailText;
  constructor(
    public keywordAnalysisService: KeywordAnalysisService,
    public multiTranslate: MultiTranslateService,
    public subTitleSubctract: SubTitleSubctractService,
    public clippingService: ClippingService
  ) { }

  url;
  format;
  onSelectFile(event) {
    debugger;
    const file = event.target.files && event.target.files[0];
    if (file) {
      this.customUrl = "C:/Users/burak/Desktop/AAHackathon/" + file.name;
      var reader = new FileReader();
      reader.readAsDataURL(file);
      if (file.type.indexOf('image') > -1) {
        this.format = 'image';
      } else if (file.type.indexOf('video') > -1) {
        this.format = 'video';
      }
      reader.onload = (event) => {
        this.url = (<FileReader>event.target).result;
      }
    }
  }

  // public arrayObject = [{ 'start': 0, 'end': 6, 'text': 'Als ich die Stadtverwaltung von Istanbul übernahm' }, { 'start': 6, 'end': 14, 'text': ' hatten wir eine Schulden von 2,5 Milliarden Dollar. Bei der Übergabe waren es 1,5' }, { 'start': 14, 'end': 20, 'text': ' Milliarden Dollar. Aber jetzt hat die Stadtverwaltung von Istanbul' }, { 'start': 20, 'end': 27, 'text': ' eine Verschuldung von drei Milliarden Dollar. Sie nehmen' }, { 'start': 27, 'end': 32, 'text': ' Gelder, die für andere Zwecke bestimmt sind,' }, { 'start': 32, 'end': 37, 'text': ' und verwenden sie, um ihre eigenen Unfähigkeiten' }, { 'start': 37, 'end': 42, 'text': ' zu verschleiern. Die Erfahrung, die wir in den vergangenen' }, { 'start': 42, 'end': 46, 'text': ' dreißig Jahren mit den Finanzbehörden gemacht haben' }, { 'start': 46, 'end': 51, 'text': ' zeigt deutlich, dass dies der Fall ist. Natürlich schauen wir während' }, { 'start': 51, 'end': 55, 'text': ' unserer Regierungsarbeit nicht auf die politische Zugehörigkeit' }, { 'start': 55, 'end': 61, 'text': ' der Personen. Unsere Ministerien und Institutionen planen und' }, { 'start': 61, 'end': 66, 'text': ' realisieren Projekte im Zusammenhang mit unseren Städten' }, { 'start': 66, 'end': 70, 'text': ' ohne Rücksicht auf die Ergebnisse der Wahlen' }, { 'start': 70, 'end': 75, 'text': ' oder die Partei des Bürgermeisters. Unser Fokus liegt allein' }, { 'start': 75, 'end': 80, 'text': ' auf den Bedürfnissen unseres Landes und unserer Städte' }, { 'start': 80, 'end': 85, 'text': ' und den Erwartungen unserer Bevölkerung.' }, { 'start': 85, 'end': 90, 'text': " Wie gestern bei der Eröffnung der von unserem Ministerium für Verkehr und Infrastruktur" }, { 'start': 90, 'end': 96, 'text': ' gebauten U-Bahn-Linie in Istanbul dargelegt, ist dies ein konkretes Beispiel für' }, { 'start': 99, 'end': 105, 'text': ' Ebenso ist das in Izmir eröffnete Stadtkrankenhaus ein weiteres Beispiel. Jedes' }, { 'start': 105, 'end': 110, 'text': ' unserer achtundsechzig Provinzen hat einen Anteil an' }, { 'start': 110, 'end': 113, 'text': ' unseren Demokratie- und Entwicklungsmaßnahmen,' }, { 'start': 113, 'end': 117, 'text': ' Investitionen, Projekten und Leistungen. Trotz dieser' }, { 'start': 117, 'end': 123, 'text': ' Tatsachen sehen manche nur den Schatten' }, { 'start': 123, 'end': 127, 'text': ' ihrer Städte und lenken die Stadt' }, { 'start': 127, 'end': 132, 'text': ' hinsichtlich der Bedürfnisse der Bevölkerung auf andere Richtungen' }, { 'start': 132, 'end': 138, 'text': ' ab. Die Menschen sind es leid, nur die' }, { 'start': 138, 'end': 142, 'text': ' Schatten zu betrachten, nur die Plakate zu' }, { 'start': 142, 'end': 146, 'text': ' sehen und nur die Propaganda zu erleben.' }, { 'start': 146, 'end': 153, 'text': ' Hoffentlich werden am einunddreißigsten März diese Schatten verschwinden' }, { 'start': 153, 'end': 159, 'text': ' und die Menschen werden den wirklichen Dienst' }, { 'start': 159, 'end': 162, 'text': ' der Stadtverwaltung erleben. Dafür setzen wir' }, { 'start': 162, 'end': 168, 'text': ' uns überall und in allen Bereichen für den' }, { 'start': 168, 'end': 172, 'text': ' Fortschritt, das Wachstum und die Stärkung unseres Landes ein.' }, { 'start': 172, 'end': 177, 'text': ' Alles andere sind leere Worte. Von unseren Bürgermeistern und Kandidaten' }, { 'start': 181, 'end': 185, 'text': ' erwarten wir, dass sie' }, { 'start': 185, 'end': 192, 'text': ' die ihnen anvertraute Verantwortung in ihrer Stadt' }, { 'start': 192, 'end': 197, 'text': ' angemessen erfüllen, ohne ihre Identität aufzugeben' }, { 'start': 197, 'end': 202, 'text': ' und Tag und Nacht zu arbeiten. Wir sind niemals nur' }, { 'start': 202, 'end': 207, 'text': ' vor den Wahlen für unsere Bürger erreichbar gewesen' }, { 'start': 207, 'end': 213, 'text': ' und werden es auch nicht sein.' }, { 'start': 216, 'end': 222, 'text': ' Wir haben niemals versucht, unsere Bevölkerung zu täuschen.' }, { 'start': 222, 'end': 226, 'text': ' Wir halten jedes Versprechen während der' }, { 'start': 226, 'end': 231, 'text': ' Wahlsaison ein und setzen jedes Projekt um.' }, { 'start': 231, 'end': 235, 'text': ' Für die Versprechen, die wir aus' }, { 'start': 235, 'end': 241, 'text': ' irgendeinem Grund nicht erfüllen konnten oder verzögert haben' }, { 'start': 241, 'end': 245, 'text': ' haben wir unsere Rechenschaft gegenüber dem Volk abgelegt. Wir' }, { 'start': 245, 'end': 249, 'text': ' erwarten von unseren Bürgermeistern, dass sie' }, { 'start': 249, 'end': 254, 'text': ' nicht nur ihre grundlegenden kommunalen Aufgaben' }, { 'start': 254, 'end': 258, 'text': ' erfüllen, sondern auch rund um die Uhr für ihre' }, { 'start': 258, 'end': 263, 'text': ' Mitbürger da sind. Wir ermutigen unsere Organisationsmitglieder,' }, { 'start': 263, 'end': 267, 'text': ' Abgeordneten und unsere Kollegen, die mit uns' }, { 'start': 267, 'end': 272, 'text': ' in der Bürokratie arbeiten, zu derselben' }, { 'start': 272, 'end': 277, 'text': ' Einstellung. Es ist undenkbar, dass jene,' }, { 'start': 277, 'end': 282, 'text': ' die für unser Land und unser Volk arbeiten,' }, { 'start': 282, 'end': 288, 'text': ' zwischen unseren Städten und unseren Menschen diskriminieren,' }, { 'start': 288, 'end': 292, 'text': ' geschweige denn politischen Fanatismus an den Tag legen. Daher' }, { 'start': 292, 'end': 297, 'text': ' betrachten wir unsere Türkei Vision für das Jahr 2023' }, { 'start': 297, 'end': 302, 'text': ' als gemeinsamen Wert unseres Landes' }, { 'start': 302, 'end': 307, 'text': ' und als gemeinsamen Traum unseres Volkes. Was für unser Land' }, { 'start': 307, 'end': 313, 'text': ' und unser Volk gut, schön und segensreich ist' }, { 'start': 313, 'end': 319, 'text': ' hat einen Platz auf unseren Herzen und Köpfen.' }, { 'start': 319, 'end': 325, 'text': ' Alles, was wir in unserem Land erreichen, alles, was wir' }, { 'start': 325, 'end': 328, 'text': ' erreichen, gehört unserem Volk.' }, { 'start': 331, 'end': 337, 'text': ' Wir widmen unserem Volk das wahre kommunale' }, { 'start': 337, 'end': 341, 'text': ' Programm für die Türkei Vision des 21. Jahrhunderts.' }, { 'start': 341, 'end': 347, 'text': ' Geschätztes Volk, wir schenken Ihnen unsere Vision, die auf' }, { 'start': 347, 'end': 352, 'text': ' unserer dreißigjährigen kommunalen Erfahrung und der globalen' }, { 'start': 352, 'end': 357, 'text': ' Stärke unseres Landes basiert. Einige der grundlegenden Prinzipien' }, { 'start': 357, 'end': 362, 'text': ' unserer Vision, die in unserem gedruckten Manifestbuch zu finden sind,' }, { 'start': 362, 'end': 368, 'text': ' möchte ich Ihnen hier kurz in Erinnerung bringen. Als AK Parti' }, { 'start': 368, 'end': 373, 'text': ' glauben wir daran, dass Demokratie und Entwicklung von unten anfangen.' }, { 'start': 373, 'end': 379, 'text': ' Durch Reformen haben wir die Verwaltungs- und Finanzkapazitäten der lokalen' }, { 'start': 379, 'end': 383, 'text': ' Regierungen gestärkt und die Menschen mit' }, { 'start': 383, 'end': 388, 'text': ' einer Dienstleistungsorientierung im Vordergrund mit ihren Träumen' }, { 'start': 388, 'end': 394, 'text': ' in Einklang gebracht. Beim Beheben von Problemen' }, { 'start': 394, 'end': 398, 'text': ' wie städtebauliche Missstände, Infrastruktur und Verkehr' }, { 'start': 398, 'end': 404, 'text': ' haben wir nur einen Anfang gemacht. In der Politik der Erschaffung' }, { 'start': 404, 'end': 409, 'text': ' von Projekten und Dienstleistungen haben wir die' }, { 'start': 409, 'end': 414, 'text': ' Standards entsprechend der zunehmenden Kraft unseres Landes' }, { 'start': 414, 'end': 418, 'text': ' und dem steigenden Lebensstandard der Bevölkerung angepasst.' }];

  ngOnInit(): void {
  }

  playVideo() {
    var myVideo: any = document.getElementById('myVideo');
    if (myVideo.paused) {
      myVideo.play();
      this.isPlay = true;
    }
    else {
      myVideo.pause();
      this.isPlay = false;
    }
  }

  pauseVideo() {

  }


  playPause() {
    var myVideo: any = document.getElementById('my_video_1');
    if (myVideo.paused) myVideo.play();
    else myVideo.pause();
  }

  runApi() {
    debugger;
    if (this.keyword) {
      const bodyKeywordanalysis =
      {
        video_path: this.customUrl,
        keyword: this.keyword,
      }
      this.keywordAnalysisService.post("api/keywordanalysis", bodyKeywordanalysis).subscribe(response => {
        this._keywordAnalysis = response;
        console.log(this._keywordAnalysis);
      })
    }

    const bodysubTopic =
    {
      video_path: this.customUrl,
    }
    this.subTitleSubctract.post("api/topics", bodysubTopic).subscribe(response => {
      this._subTopics = response;
      console.log(this._subTopics);
    })

    // const bodyMultiTranslate =
    // {
    //   path: this.customUrl,
    //   lang: "english",
    // }
    // this.multiTranslate.post("api/translate", bodyMultiTranslate).subscribe(response => {
    //   var result = response;
    //   console.log(result);
    // })
  }

  onChange(value) {
    this.selectedLang = value.target.value;
    console.log(this.selectedLang, " sdsf");
    const bodyMultiTranslate =
    {
      path: this.customUrl,
      lang: this.selectedLang,
    }
    this.multiTranslate.post("api/translate", bodyMultiTranslate).subscribe(response => {
      this._multiTranslate = JSON.parse(response[0]);
      this._translateLoop = this._multiTranslate["translations"];
      console.log(this._multiTranslate["translations"], " sdsd");
    })
  }

  cut(event) {
    let start = event[1];
    let end = event[2];
    const nameLength = 5;
    const randomName = this.generateRandomName(nameLength);
    console.log(randomName);
    const bodyClipping =
    {
      input_file: this.customUrl,
      output_file: "C:/Users/burak/Desktop/AAHackathon/" + randomName + ".mp4",
      start_time: start,
      end_time: end
    }
    this.clippingService.post("api/clipping", bodyClipping).subscribe(response => {
      console.log(response, " Bakalım");
      const Toast = Swal.mixin({        
        toast: true,
        position: "bottom-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.onmouseenter = Swal.stopTimer;
          toast.onmouseleave = Swal.resumeTimer;
        }
      });
      Toast.fire({
        icon: "success",
        title: "Kırpma işlemi başarılıyla tamamlandı."
      });
    })
  }

  skip(value) {
    debugger
    const [minutes, seconds] = value[1].slice(0, 5).split(':');
    const start = (+minutes) * 60 + (+seconds);
    console.log(start);
    const [minutes2, seconds2] = value[2].slice(0, 5).split(':');
    const duration = (+minutes2) * 60 + (+seconds2);
    console.log(start, " ", duration);
    clearTimeout(this.myTimeout);
    let playTime = duration - start;
    let video: any = document.getElementById('myVideo');
    video.currentTime = start;
    video.play();
    this.myTimeout = setTimeout(() => {
      video.pause();
    }, playTime * 1000);
  }

  skip2(value) {
    debugger
    const start = value.start;;
    console.log(start);
    let video: any = document.getElementById('myVideo');
    video.currentTime = start;
    video.play();
  }

  detailShow(value) {
    this.detailText = value.previous_text + value.current_text + value.next_text;
    Swal.fire({
      text: value.previous_text + value.current_text + value.next_text,
      confirmButtonColor: "#233446",
    })
  }

  generateRandomName(length: number): string {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    const charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
  }
}





// public myTimeout;
// @ViewChild('videoPlayer', { static: false }) videoplayer: ElementRef;
// isPlay: boolean = false;
// toggleVideo(event: any) {
//   this.videoplayer.nativeElement.play();
// }
// playPause() {
//   var myVideo: any = document.getElementById('my_video_1');
//   if (myVideo.paused) myVideo.play();
//   else myVideo.pause();
// }

// makeBig() {
//   var myVideo: any = document.getElementById('my_video_1');
//   myVideo.width = 560;
// }

// makeSmall() {
//   var myVideo: any = document.getElementById('my_video_1');
//   myVideo.width = 320;
// }

// makeNormal() {
//   var myVideo: any = document.getElementById('my_video_1');
//   myVideo.width = 420;
// }

// skip(value) {
//   clearTimeout(this.myTimeout);
//   let start = 15;
//   let duration = 25;
//   let playTime = duration - start;
//   let video: any = document.getElementById('my_video_1');
//   video.currentTime = 15;
//   video.play();
//   this.myTimeout = setTimeout(() => {
//     video.pause();
//   }, playTime * 1000);
// }

// restart() {
//   let video: any = document.getElementById('my_video_1');
//   video.currentTime = 0;
// }