package cicd

import (
	"context"
	"log"

	"github.com/runners-high/git-provider/internal/kafka"
)

// MakeCommandHandler returns a Kafka message handler that consumes cicd.commands,
// looks up the pipeline, and triggers a Jenkins build.
func MakeCommandHandler(store BuildStore, producer *kafka.EventProducer) kafka.MessageHandler {
	return func(ctx context.Context, topic string, key, value []byte) error {
		cmd, err := kafka.ParseEvent[kafka.TriggerBuildCommand](value)
		if err != nil {
			return err
		}

		if cmd.Type != "trigger_build" {
			log.Printf("cicd consumer: unknown command type %q, skipping", cmd.Type)
			return nil
		}

		log.Printf("cicd command: trigger_build pipeline=%s branch=%s exec=%s", cmd.PipelineID, cmd.Branch, cmd.ExecutionID)

		p, err := store.GetPipeline(cmd.PipelineID)
		if err != nil {
			log.Printf("cicd consumer: pipeline not found %s: %v", cmd.PipelineID, err)
			return nil // don't retry — pipeline doesn't exist
		}

		_, err = TriggerAndPoll(ctx, TriggerRequest{
			Pipeline:    p,
			Branch:      cmd.Branch,
			CommitSHA:   cmd.CommitSHA,
			ExecutionID: cmd.ExecutionID,
		}, store, producer)
		if err != nil {
			log.Printf("cicd consumer: trigger failed pipeline=%s: %v", cmd.PipelineID, err)
		}

		return nil
	}
}
