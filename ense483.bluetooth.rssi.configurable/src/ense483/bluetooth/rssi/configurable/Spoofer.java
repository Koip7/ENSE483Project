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
    
    private static final String PUBLISH_RATE_PROP_NAME = "publish.rate";
    
    private static final String RSSI_DATA_PROP_NAME = "rssi.node";
    
    private static final int NUMBER_OF_NODES = 8;

    private final ScheduledExecutorService worker;
    private ScheduledFuture<?> handle;
    
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
/*
    protected void activate(ComponentContext componentContext) {
        s_logger.info("Bundle " + APP_ID + " has started!");
    }
*/
    
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

        // try to kick off a new job
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

    // ----------------------------------------------------------------
    //
    // Private Methods
    //
    // ----------------------------------------------------------------

    /**
     * Called after a new set of properties has been configured on the service
     */
    private void doUpdate(boolean onUpdate) {
        // cancel a current worker handle if one if active
    	/*
        if (this.handle != null) {
            this.handle.cancel(true);
        }

        // schedule a new worker based on the properties of the service
        int pubrate = (Integer) this.properties.get(PUBLISH_RATE_PROP_NAME);
        this.handle = this.worker.scheduleAtFixedRate(new Runnable() {

            @Override
            public void run() {
                Thread.currentThread().setName(getClass().getSimpleName());
                doPublish();
            }
        }, 0, pubrate, TimeUnit.SECONDS);
        */
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
        /*
        for (int i = 0 ; i < NUMBER_OF_NODES; i++) {
        	
        	String prop_name = RSSI_DATA_PROP_NAME + Integer.toString(i);
        	logger.info("getting " + prop_name);
        	
        	int rssi_value = (Integer) this.properties.get(prop_name);
        	payload.addMetric("RSSI" + Integer.toString(i), rssi_value);
        }
       */ 
        payload.addMetric("01", (Integer) this.properties.get("rssi.node01"));
        payload.addMetric("02", (Integer) this.properties.get("rssi.node02"));
        payload.addMetric("03", (Integer) this.properties.get("rssi.node03"));
        payload.addMetric("04", (Integer) this.properties.get("rssi.node04"));
        payload.addMetric("05", (Integer) this.properties.get("rssi.node05"));
        
        payload.addMetric("12", (Integer) this.properties.get("rssi.node12"));
        payload.addMetric("13", (Integer) this.properties.get("rssi.node13"));
        payload.addMetric("14", (Integer) this.properties.get("rssi.node14"));
        payload.addMetric("15", (Integer) this.properties.get("rssi.node15"));
        
        payload.addMetric("23", (Integer) this.properties.get("rssi.node23"));
        payload.addMetric("24", (Integer) this.properties.get("rssi.node24"));
        payload.addMetric("25", (Integer) this.properties.get("rssi.node25"));
        
        payload.addMetric("34", (Integer) this.properties.get("rssi.node34"));
        payload.addMetric("35", (Integer) this.properties.get("rssi.node35"));
        
        payload.addMetric("45", (Integer) this.properties.get("rssi.node45"));

        
        // Add the temperature as a metric to the payload
        /*
        payload.addMetric("RSSI1", 3.0F);
        payload.addMetric("RSSI2", 5.0F);
        payload.addMetric("RSSI3", 30.0F);

        int code = this.random.nextInt();
        if (this.random.nextInt() % 5 == 0) {
            payload.addMetric("errorCode", code);
        } else {
            payload.addMetric("errorCode", 0);
        }
	*/
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
