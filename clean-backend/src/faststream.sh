      sh -c "
        echo 'Waiting for app API to be ready...';
        while ! curl -s --fail http://app:8000/docs > /dev/null; do
          sleep 2;
        done;
        echo 'App is ready. Starting FastStream worker...';
        faststream run clean_backend/fs_serve_app:faststream_app
      "