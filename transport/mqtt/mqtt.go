package mqtt

import (
	"flag"
	"fmt"
	MQTT "github.com/eclipse/paho.mqtt.golang"
	"github.com/netsampler/goflow2/v2/producer"
	"github.com/netsampler/goflow2/v2/transport"
	log "github.com/sirupsen/logrus"
	"sync"
)

type MqttDriver struct {
	brokerUrl string
	client    MQTT.Client
	clientId  string
	topic     string
	lock      *sync.RWMutex
	q         chan bool
}

func (d *MqttDriver) Prepare() error {
	flag.StringVar(&d.brokerUrl, "transport.mqtt.broker", "tcp://127.0.0.1:1883", "mqtt broker url")
	flag.StringVar(&d.clientId, "transport.mqtt.id", "goflow2", "mqtt client id")
	flag.StringVar(&d.topic, "transport.mqtt.topic", "flow", "mqtt topic")
	return nil
}

func (d *MqttDriver) Init() error {
	opts := MQTT.NewClientOptions().AddBroker(d.brokerUrl)
	opts.SetClientID(d.clientId)
	client := MQTT.NewClient(opts)
	d.client = client
	d.client.Connect()
	return nil
}

func (d *MqttDriver) Close() error {
	d.client.Disconnect(0)
	return nil
}

func (d *MqttDriver) Send(key, data []byte, msg producer.ProducerMessage) error {
	topic := d.topic
	_ = msg
	if dataIf, ok := msg.(interface{ TopicSublevel() string }); ok {
		sublevel_topic := dataIf.TopicSublevel()
		topic = fmt.Sprintf("%s/%s", d.topic, sublevel_topic)
	}

	log.Debug("mqtt send one")
	d.client.Publish(topic, 0, false, data)
	return nil
}

/*
func example() {

	client := MQTT.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	topic := "test/topic"
	text := "Hello, MQTT!"

	token := client.Publish(topic, 0, false, text)
	token.Wait()

	client.Disconnect(250)
}
*/

func init() {
	d := &MqttDriver{
		lock: &sync.RWMutex{},
	}
	transport.RegisterTransportDriver("mqtt", d)
}
