#/bin/bash

today=$(date -I)
cd $EXPORT_ROOT

for directory in $(ls); do
  if [ "${directory}" \< "${today}" ]; then
    echo "Archiving ${directory}"
    tar -czf $directory.tar.gz $directory --remove-files
    $RCLONE_PATH move $directory.tar.gz ${RCLONE_REMOTE}
  fi
done
