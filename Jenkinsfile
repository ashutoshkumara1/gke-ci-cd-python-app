pipeline {
    agent any
	
	environment {
		PROJECT_ID = 'optimistic-yeti-363002' //Project ID From Google Cloud Project
		CLUSTER_NAME = 'k8s-cluster' //Kubernetes Engine Cluster Name
		LOCATION = 'us-central1-c' //Kubernetes Engine Cluster Location
		CREDENTIAL_ID = 'kubernetes' //Credential Id Which Created in Jenkins for Kubernetes Credentials		
	}
	
    stages {
	    stage('Scm Checkout') {
		    steps {
			    checkout scm
		    }
	    }

	    //Buliding Docker Image
    	stage('Build Docker Image') {
        	steps {
            	script {
                	img = registry + ":${env.BUILD_ID}"
                	println ("${img}")
                	dockerImage = docker.build("${img}")
            	}
        	}
    	}
	    
	    stage("Push Docker Image") {
		    steps {
			    script {
				    echo "Push Docker Image"
				    withCredentials([string(credentialsId: 'DOCKER_HUB_CREDENTIALS', variable: 'DOCKER_HUB_CREDENTIALS')]) {
            				sh "docker login -u ashutosha1 -p ${DOCKER_HUB_CREDENTIALS}"
				    }
				        myimage.push("${env.BUILD_ID}")
				    
			    }
		    }
	    }
	    
	    stage('Deploy to K8s') {
		    steps{
			    echo "Deployment started ..."
			    sh 'ls -ltr'
			    sh 'pwd'
			    sh "sed -i 's/tagversion/${env.BUILD_ID}/g' serviceLB.yaml"
				sh "sed -i 's/tagversion/${env.BUILD_ID}/g' deployment.yaml"
			    echo "Start deployment of serviceLB.yaml"
			    step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'serviceLB.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
				echo "Start deployment of deployment.yaml"
				step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'deployment.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
			    echo "Deployment Finished ..."
		    }
	    }
    }
}
