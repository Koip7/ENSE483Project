/*Justin Smith
 * ENSE483
 * Class Project
 * 
 * This file defines the Spoofer plugin
 * This plugin retrieves configured spoof data stating RSSI values between different nodes
 * It then uses the configured cloud service to send the data over the configured protocol
 * Currently this is only tested with the MQTT protocol
 */

package ense483.bluetooth.rssi.configurable;

import java.util.Date;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import org.eclipse.kura.cloudconnection.listener.CloudConnectionListener;
import org.eclipse.kura.cloudconnection.listener.CloudDeliveryListener;
import org.eclipse.kura.cloudconnection.message.KuraMessage;
import org.eclipse.kura.cloudconnection.publisher.CloudPublisher;
import org.eclipse.kura.configuration.ConfigurableComponent;
import org.eclipse.kura.message.KuraPayload;
import org.osgi.service.component.ComponentContext;
import org.osgi.service.component.ComponentException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Spoofer implements ConfigurableComponent, CloudConnectionListener, CloudDeliveryListener {
    private static final Logger logger = LoggerFactory.getLogger(Spoofer.class);
    
    private static final String APP_ID = "ense483.bluetooth.rssi.configurable.Spoofer";
    private Map<String, Object> properties;

    //private static final int NUMBER_OF_NODES = 8;

    private final ScheduledExecutorService worker;
    
    private CloudPublisher cloudPublisher;
    
    public Spoofer() {
    	super();
    	this.worker = Executors.newSingleThreadScheduledExecutor();
    }
    
    public void setCloudPublisher(CloudPublisher cloudPublisher) {
        this.cloudPublisher = cloudPublisher;
        this.cloudPublisher.registerCloudConnectionListener(Spoofer.this);
        this.cloudPublisher.registerCloudDeliveryListener(Spoofer.this);
    }

    public void unsetCloudPublisher(CloudPublisher cloudPublisher) {
        this.cloudPublisher.unregisterCloudConnectionListener(Spoofer.this);
        this.cloudPublisher.unregisterCloudDeliveryListener(Spoofer.this);
        this.cloudPublisher = null;
    }

    protected void activate(ComponentContext componentContext, Map<String, Object> properties) {
    	logger.info("Activating Spoofer...");

        this.properties = properties;
        for (Entry<String, Object> property : properties.entrySet()) {
            logger.info("Update - {}: {}", property.getKey(), property.getValue());
        }

        try {
            doUpdate(false);
        } catch (Exception e) {
            logger.error("Error during component activation", e);
            throw new ComponentException(e);
        }
        logger.info("Activating Spoofer... Done.");
    }

    protected void deactivate(ComponentContext componentContext) {
        logger.debug("Deactivating Spoofer...");

        // shutting down the worker and cleaning up the properties
        this.worker.shutdown();

        logger.debug("Deactivating Spoofer... Spoofer.");
    }

    public void updated(Map<String, Object> properties) {
        logger.info("Updated Spoofer...");

        // store the properties received
        this.properties = properties;
        for (Entry<String, Object> property : properties.entrySet()) {
            logger.info("Update - {}: {}", property.getKey(), property.getValue());
        }

        doUpdate(true);
        logger.info("Updated Spoofer... Done.");
    }
    

    // ----------------------------------------------------------------
    //
    // Cloud Application Callback Methods
    //
    // ----------------------------------------------------------------

    @Override
    public void onConnectionLost() {
        // TODO Auto-generated method stub

    }

    @Override
    public void onConnectionEstablished() {
        // TODO Auto-generated method stub

    }

    @Override
    public void onMessageConfirmed(String messageId) {
        // TODO Auto-generated method stub

    }

    @Override
    public void onDisconnected() {
        // TODO Auto-generated method stub

    }

    /**
     * Called after a new set of properties has been configured on the service
     */
    private void doUpdate(boolean onUpdate) {
    	//when the configuration of the plugin is changed send out data over cloud publisher
        doPublish();
    }

    /**
     * Called at the configured rate to publish the next temperature measurement.
     */
    private void doPublish() {
        if (this.cloudPublisher == null) {
            logger.info("No cloud publisher selected. Cannot publish!");
            return;
        }

        // Allocate a new payload
        KuraPayload payload = new KuraPayload();

        // Timestamp the message
        payload.setTimestamp(new Date());
        
       //TODO: Do this programically instead of hardcoded
        //packing of the RSSI data as read from the configuration data
        payload.addMetric("01", (Integer) this.properties.get("rssi.node01"));
        payload.addMetric("02", (Integer) this.properties.get("rssi.node02"));
        payload.addMetric("03", (Integer) this.properties.get("rssi.node03"));
        payload.addMetric("04", (Integer) this.properties.get("rssi.node04"));
        payload.addMetric("05", (Integer) this.properties.get("rssi.node05"));
        payload.addMetric("06", (Integer) this.properties.get("rssi.node06"));
        payload.addMetric("07", (Integer) this.properties.get("rssi.node07"));
        payload.addMetric("08", (Integer) this.properties.get("rssi.node08"));
        payload.addMetric("09", (Integer) this.properties.get("rssi.node09"));
        
        payload.addMetric("12", (Integer) this.properties.get("rssi.node12"));
        payload.addMetric("13", (Integer) this.properties.get("rssi.node13"));
        payload.addMetric("14", (Integer) this.properties.get("rssi.node14"));
        payload.addMetric("15", (Integer) this.properties.get("rssi.node15"));
        payload.addMetric("16", (Integer) this.properties.get("rssi.node16"));
        payload.addMetric("17", (Integer) this.properties.get("rssi.node17"));
        payload.addMetric("18", (Integer) this.properties.get("rssi.node18"));
        payload.addMetric("19", (Integer) this.properties.get("rssi.node19"));
        
        payload.addMetric("23", (Integer) this.properties.get("rssi.node23"));
        payload.addMetric("24", (Integer) this.properties.get("rssi.node24"));
        payload.addMetric("25", (Integer) this.properties.get("rssi.node25"));
        payload.addMetric("26", (Integer) this.properties.get("rssi.node26"));
        payload.addMetric("27", (Integer) this.properties.get("rssi.node27"));
        payload.addMetric("28", (Integer) this.properties.get("rssi.node28"));
        payload.addMetric("29", (Integer) this.properties.get("rssi.node29"));
        
        KuraMessage message = new KuraMessage(payload);

        // Publish the message
        try {
            this.cloudPublisher.publish(message);
            logger.info("Published message: {}", payload);
        } catch (Exception e) {
            logger.error("Cannot publish message: {}", message, e);
        }
    }
}
