#include <RH_RF95.h>
#include<DS3232RTC.h>
#include<Streaming.h>
RH_RF95 rf95;
DS3232RTC omnitrix;
#define DEBUG true
void setup(){
  Serial.begin(9600);
  //tempo stuff
  setSyncProvider(RTC.get);
  if(timeStatus()!=timeSet){
    Serial.println("FAIL!");
  }
  Serial.println("Setup finished");
  // end time stuff
  // Lora Stuff
  while(!Serial); //Wait for serial port to be avaliable
  if(!rf95.init())
    Serial.println("RF95 init failed");
  rf95.setTxPower(20,false); //seta potencia de transmissao
  rf95.setFrequency(915.0);
  rf95.setSignalBandwidth(500000) ;
  rf95.setSpreadingFactor(12) ;
  //end Lora Stuff
}

void loop(){
  int valor_do_sensor;
  String tempo;
  int parametro;
  for(parametro = 5; parametro < 9; parametro++){
    if(parametro == 5) {rf95.setCodingRate4(5);} 
    if(parametro == 6) {rf95.setCodingRate4(6);} 
    if(parametro == 7) {rf95.setCodingRate4(7);} 
    if(parametro == 8) {rf95.setCodingRate4(8);} 
    //Mensagem de controle
    for(int controle = 0; controle < 20; controle++){
     //   delay(500);
      String control_mensage = ("CR:"+String(parametro));
      Serial.println(control_mensage);
      uint8_t valueToSend[control_mensage.length()+1];
      control_mensage.toCharArray(valueToSend,control_mensage.length()+1);
      rf95.send ( valueToSend ,sizeof(valueToSend));
      rf95.waitPacketSent();
    }
    //Pacotes enviados
    for(int id = 0; id < 100; id++){
      delay(100);
      valor_do_sensor = getSensorValue().toInt();
      tempo = pegaTempo();
      String payload = (String(id) + '-' + String(valor_do_sensor) + '-' + String(tempo) + '-' + String(parametro));
      //String payload = "teste"; 
      Serial.println(payload);
      uint8_t valueToSend[payload.length()+1];
      payload.toCharArray(valueToSend,payload.length()+1);
      rf95.send ( valueToSend ,sizeof(valueToSend));
      rf95.waitPacketSent();
    }
  }
  //Reset 
  parametro = 5;
  delay(1000);
}

String getTime(){
  time_t t = omnitrix.get();
}

String  getSensorValue(){
  float sensorValue = analogRead(0);
  String aux = String(sensorValue,1);   
  return aux;
}

String pegaTempo(){
  time_t t;
  t = now();
  String horario = "";
  horario.concat(printI00 (hour(t),':')) ;
  horario.concat(printI00 (minute(t),':'));
  horario.concat(printI00 (second(t),"")) ;
  return horario;
}

String printI00 ( int val , char delim ){
  String t_unit = "";
  if (val < 10 ) t_unit.concat('0') ;
  int decimal = val;
  t_unit.concat(String(decimal)) ;
  if ( delim>0) t_unit.concat(delim) ;
  return t_unit;
}
